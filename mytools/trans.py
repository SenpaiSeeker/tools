import random
import string

from gpytranslate import SyncTranslator


def random_name():
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return random_string + ".mp3"


class Translate(SyncTranslator):
    def ConvertLang(self, msg, lang="id"):
        trans = self.translate(msg, targetlang=lang)
        return trans.text

    def TextToSpeech(self, text):
        filename = random_name()

        with open(filename, "wb") as file:
            self.tts(text, file=file)

        return filename
