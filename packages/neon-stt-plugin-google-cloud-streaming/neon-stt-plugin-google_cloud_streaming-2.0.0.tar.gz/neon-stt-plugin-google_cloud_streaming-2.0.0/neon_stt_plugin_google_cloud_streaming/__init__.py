# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from copy import copy
from queue import Queue
from threading import Event

import google.api_core.retry
from google.cloud import speech
from google.oauth2.service_account import Credentials
from ovos_utils.log import LOG
from ovos_plugin_manager.templates.stt import StreamingSTT, StreamThread

from neon_stt_plugin_google_cloud_streaming.languages import stt_config


class GoogleCloudStreamingSTT(StreamingSTT):
    """
        Streaming STT interface for Google Cloud Speech-To-Text
        To use pip install google-cloud-speech and add the
        Google API key to local mycroft.conf file. The STT config
        will look like this:

        "stt": {
            "module": "google_cloud_streaming",
            "google_cloud_streaming": {
                "credential": {
                    "json": {
                        # Paste Google API JSON here
        ...

    """

    def __init__(self, config=None, **kwargs):
        super(GoogleCloudStreamingSTT, self).__init__(config=config)

        # override language with module specific language selection
        self.language = self.config.get('lang') or self.lang
        self.queue = None

        creds = self.config.get("credential")

        if creds:
            creds = creds.get('json') or creds
            LOG.debug(f"Got credentials: {creds}")
            credentials = Credentials.from_service_account_info(creds)
        else:
            try:
                from neon_utils.authentication_utils import find_neon_google_keys
                credential_json = find_neon_google_keys()
                credentials = Credentials.from_service_account_info(credential_json)
            except Exception as e:
                LOG.error(e)
                credentials = None

        self.client = speech.SpeechClient(credentials=credentials)
        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language,
            max_alternatives=3
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=False
        )

    def create_streaming_thread(self):
        self.queue = Queue()
        return GoogleStreamThread(
            self.queue,
            self.language,
            self.client,
            self.streaming_config
        )

    @property
    def available_languages(self) -> set:
        return set(stt_config.keys())

    def transcribe(self, *args, **kwargs):
        self.queue.put(None)
        self.stream.results_event.wait()
        result = copy(self.stream.transcriptions)
        self.stream_stop()
        return result or []


class GoogleStreamThread(StreamThread):
    def __init__(self, queue, lang, client, streaming_config):
        super().__init__(queue, lang)
        self.name = "StreamThread"
        self.client = client
        self.retry = google.api_core.retry.Retry(timeout=30)
        self.timeout = 30
        self.streaming_config = streaming_config
        self.results_event = Event()
        self.transcriptions = []

    def handle_audio_stream(self, audio, language):
        req = (speech.StreamingRecognizeRequest(audio_content=x) for x in audio)
        responses = self.client.streaming_recognize(self.streaming_config, req,
                                                    timeout=self.timeout,
                                                    retry=self.retry)
        # Responses are yielded, but we will return once the first sentence is transcribed
        for res in responses:
            for result in res.results:
                LOG.debug(result)
            if res.results and res.results[0].is_final:
                self.transcriptions = []
                for alternative in res.results[0].alternatives:
                    transcription = alternative.transcript
                    confidence = alternative.confidence
                    self.transcriptions.append((transcription, confidence))
        LOG.debug(self.transcriptions)
        self.results_event.set()
        if self.transcriptions:
            self.text = self.transcriptions[0][0]  # Backwards compat.
        return self.transcriptions

    def finalize(self):
        self.results_event.wait()
        return super().finalize()
