from logging import getLogger
from os import getenv
from random import choice

from dotenv import load_dotenv
from requests import get
from yaml import safe_load

load_dotenv()
_SOURCES_FILE = getenv("SOURCES_FILE")
with open(_SOURCES_FILE) as sources_file:
    _SOURCES = safe_load(sources_file)
_MEDIA_SOURCES = _SOURCES["media"]
_TEXT_SOURCES = _SOURCES["text"]

_logger = getLogger(__name__)


def get_random_image_url() -> str:
    return _get_resource(_MEDIA_SOURCES)


def get_pasta() -> str:
    return _get_resource(_TEXT_SOURCES)


def _get_resource(sources: list[dict[str, str]]) -> str:
    source = choice(sources)
    source_url = source["url"]
    _logger.info(f"Using [{source_url}]")
    item = get(source_url).json()
    source_key = source["key"]
    return item[source_key].strip()
