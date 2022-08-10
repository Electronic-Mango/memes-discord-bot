from logging import getLogger
from os import getenv
from random import choice
from typing import Any

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
    response_json = _load_resource_json(source)
    return _extract_resource_from_json(response_json, source["keys"])


def _load_resource_json(source: dict[str, str]) -> dict[str, Any]:
    source_url = source["url"]
    _logger.info(f"Using [{source_url}]")
    return get(source_url).json()


def _extract_resource_from_json(json_resource: Any, keys: list[str]) -> str:
    resource = json_resource
    for key in keys:
        resource = resource[key]
    return resource
