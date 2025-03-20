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

import requests

from urllib.parse import quote
from typing import Optional
from ovos_plugin_manager.templates.tts import TTS, TTSValidator, RemoteTTSException

from neon_tts_plugin_coqui_remote.configs import languages


class CoquiRemoteTTS(TTS):
    # TODO: Update to query remote API
    langs = languages
    public_servers = ['https://coqui.neonaiservices.com',
                      'https://coqui.neonaibeta.com',
                      ]

    def __init__(self, lang: str = "en", config: dict = None,
                 api_path: str = '/synthesize'):
        config = config or dict()
        TTS.__init__(self, config=config, validator=CoquiRemoteTTSValidator(self))
        self.api_path = api_path or "/"
        self.url = config.get("url", "").rstrip("/")

    def get_tts(self, sentence: str, output_file: str,
                speaker: Optional[dict] = None,
                lang: Optional[str] = None) -> (str, Optional[str]):
        """
        Get Synthesized audio
        Args:
            sentence: string to synthesize
            output_file: path to output audio file
            speaker: optional dict speaker data
            lang: optional lang override
        Returns:
            tuple wav_file, optional phonemes
        """
        speaker = speaker or dict()
        lang = lang or speaker.get('language') or self.lang

        if not self.url:
            resp = self._get_from_public_servers(lang, sentence)
        else:
            resp = requests.get(f'{self.url}{self.api_path}/{quote(sentence)}',
                                params={'lang': lang})
            if not resp.ok:
                raise RemoteTTSException(resp.text)
        with open(output_file, 'wb') as f:
            f.write(resp.content)
        return output_file, None

    @property
    def available_languages(self):
        return set(self.langs.keys())

    def _get_from_public_servers(self, lang, sentence):
        for url in self.public_servers:
            try:
                r = requests.get(f'{url}{self.api_path}/{quote(sentence)}',
                                 params={'lang': lang})
                if r.ok:
                    return r
            except:
                continue
        raise RemoteTTSException(f"All Coqui public servers are down, "
                                 f"please self host Coqui")


class CoquiRemoteTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CoquiRemoteTTSValidator, self).__init__(tts)

    def validate_lang(self):
        if self.tts.lang.split('-')[0] not in CoquiRemoteTTS.langs:
            raise KeyError(f"Language isn't supported: {self.tts.lang}")

    def validate_dependencies(self):
        # TODO: Optionally check dependencies or raise
        pass

    def validate_connection(self):
        # TODO: Optionally check connection to remote service or raise
        pass

    def get_tts_class(self):
        return CoquiRemoteTTS
