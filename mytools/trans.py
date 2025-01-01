import random
import string

import gtts
from gpytranslate import SyncTranslator


class Translate(SyncTranslator):
    def ConvertLang(self, msg, lang="id"):
        trans = self.translate(msg, targetlang=lang)
        return trans.text

    def TextToSpeech(self, text):
        filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".oog"

        speech = gtts.gTTS(text, lang="id")
        speech.save(filename)

        return filename
