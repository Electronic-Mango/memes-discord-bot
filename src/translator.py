"""
Module handling text translation.
"""

from logging import getLogger

from deep_translator import GoogleTranslator

_logger = getLogger(__name__)


def translate(source: str, target_language: str) -> str:
    """Translate text to a given language"""
    _logger.info(f"Translating text to [{target_language}]")
    return GoogleTranslator(target=target_language).translate(source)


def is_valid_language(language: str) -> bool:
    """Check if given language can be used as a target language for translation"""
    _logger.info(f"Checking validity [{language}]")
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    return language in supported_languages or language in supported_languages.values()
