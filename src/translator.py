from googletrans import LANGUAGES, Translator

_translator = Translator()


def translate(source: str, target_language: str) -> str:
    return _translator.translate(text=source, dest=target_language).text


def is_valid_language(language: str) -> bool:
    return language in LANGUAGES or language in LANGUAGES.values()


def detect_language(source: str) -> str:
    return _translator.detect(source).lang
