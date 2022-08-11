from logging import getLogger

from deep_translator import GoogleTranslator

_logger = getLogger(__name__)


def translate(source: str, target_language: str) -> str:
    _logger.info(f"Translating text to [{target_language}]")
    return GoogleTranslator(target=target_language).translate(source)


def is_valid_language(language: str) -> bool:
    _logger.info(f"Checking validity [{language}]")
    supported_languages = GoogleTranslator().get_supported_languages()
    return language in supported_languages or language in supported_languages.values()
