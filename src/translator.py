"""
Module handling text translation.
"""

from logging import getLogger

from deep_translator import GoogleTranslator
from more_itertools import sliced

_MAX_TRANSLATED_TEXT_SIZE = 4999
_SUPPORTED_LANGUAGES = [
    *GoogleTranslator().get_supported_languages(),
    *GoogleTranslator().get_supported_languages(as_dict=True).values(),
]

_logger = getLogger(__name__)


async def translate(source: str, target_language: str) -> str:
    """Translate text to a given language"""
    _logger.info(f"Translating text to [{target_language}]")
    return "".join(
        GoogleTranslator(target=target_language).translate(slice).strip()
        for slice in sliced(source, _MAX_TRANSLATED_TEXT_SIZE)
    )


def is_valid_language(language: str) -> bool:
    """Check if given language can be used as a target language for translation"""
    _logger.info(f"Checking validity [{language}]")
    return language in _SUPPORTED_LANGUAGES


def supported_languages_matches(input: str) -> list[str]:
    """Returns a list of potentially matching languages for a given input"""
    return [language for language in _SUPPORTED_LANGUAGES if language.startswith(input)]
