from logging import getLogger
from os import getenv
from random import choice

from dotenv import load_dotenv
from requests import get
from yaml import safe_load

load_dotenv()
_SOURCES_FILE = getenv("SOURCES_FILE")
with open(_SOURCES_FILE) as sources_file:
    _MEDIA_SOURCES = safe_load(sources_file)["text"]

_logger = getLogger(__name__)


def get_pasta() -> str:
    source_url = choice(_MEDIA_SOURCES)
    _logger.info(f"Using [{source_url}]")
    item = get(source_url).json()
    return item["selftext"].strip()
