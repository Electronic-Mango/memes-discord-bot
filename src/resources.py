from functools import reduce
from logging import getLogger
from random import choice
from typing import Any

from requests import get
from yaml import safe_load

from settings import SOURCES_FILE

with open(SOURCES_FILE) as sources_file:
    _SOURCES = safe_load(sources_file)
_MEDIA_SOURCES = _SOURCES["media"]
_TEXT_SOURCES = _SOURCES["text"]

_logger = getLogger(__name__)


def get_random_media_url() -> str:
    return _get_resource(_MEDIA_SOURCES)


def get_random_text() -> str:
    return _get_resource(_TEXT_SOURCES)


def _get_resource(sources: list[dict[str, Any]]) -> str:
    source = choice(sources)
    response_json = _load_resource_json(source)
    return _extract_resource_from_json(response_json, source["keys"])


def _load_resource_json(source: dict[str, Any]) -> dict[str, Any]:
    source_url = source["url"]
    source_headers = _parse_headers(source)
    _logger.info(f"Using URL=[{source_url}] headers={source_headers}")
    return get(source_url, headers=source_headers).json()


def _parse_headers(source: dict[str, Any]) -> dict[str, str]:
    headers = source.get("headers", [])
    return {header["name"]: header["value"] for header in headers}


def _extract_resource_from_json(json_resource: Any, keys: list[str]) -> str:
    return reduce(lambda json, key: json[key], keys, json_resource)
