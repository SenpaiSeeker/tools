from gpytranslate import SyncTranslator


class Translate(SyncTranslator):
    def msg(self, msg, lang="id"):
        trans = self.translate(msg, targetlang=lang)
        return trans.text
