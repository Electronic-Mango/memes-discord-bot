from googletrans import Translator

_translator = Translator()


def translate(source: str, target_language: str) -> str:
    return _translator.translate(text=source, dest=target_language).text
