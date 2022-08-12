"""
Module responsible for loading random media URLs and texts from external REST APIs.
Media can be images, GIFs, videos, etc.
Sources for each are defined in "sources.yml" file, or whichever is defined in "settings.yml".
"""

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
_DEFAULT_LANGUAGE = "en"

_logger = getLogger(__name__)


def get_random_media_url() -> str:
    """Get a random media URL"""
    source = choice(_MEDIA_SOURCES)
    return _get_resource(source)


def get_random_text() -> tuple[str, str]:
    """Get a random text and its language"""
    source = choice(_TEXT_SOURCES)
    return _get_resource(source), source.get("language", _DEFAULT_LANGUAGE)


def _get_resource(source: dict[str, Any]) -> str:
    response_json = _load_resource_json(source)
    return _extract_resource_from_json(response_json, source.get("keys", []))


def _load_resource_json(source: dict[str, Any]) -> dict[str, Any]:
    source_url = source["url"]
    source_headers = _parse_headers_from_source(source)
    _logger.info(f"Using URL=[{source_url}] headers={source_headers}")
    return get(source_url, headers=source_headers).json()


def _parse_headers_from_source(source: dict[str, Any]) -> dict[str, str]:
    headers = source.get("headers", [])
    return {header["name"]: header["value"] for header in headers}


def _extract_resource_from_json(json_resource: Any, keys: list[str]) -> str:
    return reduce(lambda json, key: json[key], keys, json_resource)
