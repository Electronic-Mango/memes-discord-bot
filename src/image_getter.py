from logging import getLogger
from os import getenv
from random import choice
from requests import get

from dotenv import load_dotenv
from yaml import safe_load

load_dotenv()
_MEDIA_SOURCES_FILE = getenv("MEDIA_SOURCES_FILE")

_logger = getLogger(__name__)


def get_random_image_url() -> str:
    feed_source = _get_random_source()
    item = get(feed_source).json()
    return item["url"]


def _get_random_source() -> str:
    with open(_MEDIA_SOURCES_FILE) as sources_file:
        sources = safe_load(sources_file)
    source_name, source_url = choice(list(sources.items()))
    _logger.info(f"Using [{source_name}] [{source_url}]")
    return source_url
