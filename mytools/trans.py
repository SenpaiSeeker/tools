from gpytranslate import SyncTranslator


class Translate(SyncTranslator):
    def ConvertLang(self, msg, lang="id"):
        trans = self.translate(msg, targetlang=lang)
        return trans.text

    def TextToSpeech(self, text, name):
        with open(name, "wb") as file:
            self.tts(text, file=file)
