"""
Module responsible for loading random media URLs and texts from external REST APIs.
Media can be images, GIFs, videos, etc.
Sources for each are defined in "sources.yml" file, or whichever is defined in "settings.yml".
"""

from functools import reduce
from logging import getLogger
from random import choice
from typing import Any

from aiohttp import ClientSession
from yaml import safe_load

from settings import SOURCES_FILE

_MEDIA_SOURCES = "media"
_TEXT_SOURCES = "text"
_DEFAULT_LANGUAGE = "en"

_logger = getLogger(__name__)


async def get_random_media_url_and_title() -> tuple[str, str]:
    """Get a random media URL and its title"""
    source = choice(_load_sources(_MEDIA_SOURCES))
    response = await _load_resource_json(source)
    url = _extract_resource(response, source.get("keys", []))
    title = _extract_resource(response, source["title_keys"]) if "title_keys" in source else None
    return url, title


async def get_random_text() -> tuple[str, str]:
    """Get a random text and its language"""
    source = choice(_load_sources(_TEXT_SOURCES))
    response = await _load_resource_json(source)
    text = _extract_resource(response, source.get("keys", []))
    language = source.get("language", _DEFAULT_LANGUAGE)
    return text, language


def _load_sources(field: str) -> Any:
    with open(SOURCES_FILE) as sources_file:
        return safe_load(sources_file)[field]


async def _load_resource_json(source: dict[str, Any]) -> dict[str, Any]:
    source_url = source["url"]
    source_headers = _parse_headers_from_source(source)
    _logger.info(f"Using URL=[{source_url}] headers={source_headers}")
    return await _get_request_to_json(source_url, source_headers)


def _parse_headers_from_source(source: dict[str, Any]) -> dict[str, str]:
    headers = source.get("headers", [])
    return {header["name"]: header["value"] for header in headers}


async def _get_request_to_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    async with ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


def _extract_resource(json_resource: Any, keys: list[str]) -> str:
    return reduce(lambda json, key: json[key], keys, json_resource)
