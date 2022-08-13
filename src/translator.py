"""
Module handling text translation.
"""

from logging import getLogger

from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = [
    *GoogleTranslator().get_supported_languages(),
    *GoogleTranslator().get_supported_languages(as_dict=True).values(),
]

_logger = getLogger(__name__)


def translate(source: str, target_language: str) -> str:
    """Translate text to a given language"""
    _logger.info(f"Translating text to [{target_language}]")
    return GoogleTranslator(target=target_language).translate(source)


# TODO Does this needs to be a thing, if "supported languages" is public?
def is_valid_language(language: str) -> bool:
    """Check if given language can be used as a target language for translation"""
    _logger.info(f"Checking validity [{language}]")
    return language in SUPPORTED_LANGUAGES
