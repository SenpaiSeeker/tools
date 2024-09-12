import random
import string

import gtts
from gpytranslate import SyncTranslator


def random_name():
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return random_string + ".oog"


class Translate(SyncTranslator):
    def ConvertLang(self, msg, lang="id"):
        trans = self.translate(msg, targetlang=lang)
        return trans.text

    def TextToSpeech(self, text):
        filename = random_name()

        speech = gtts.gTTS(text, lang="id")
        speech.save(filename)

        return filename
