from logging import getLogger
from os import getenv
from random import choice

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from feedparser import parse
from yaml import safe_load

load_dotenv()
_MEDIA_SOURCES_FILE = getenv("MEDIA_SOURCES_FILE")

_logger = getLogger(__name__)


def get_random_image_url() -> str:
    feed_source = _get_random_source()
    feed = parse(feed_source)
    random_item = choice(feed.entries)
    media_source = BeautifulSoup(random_item.summary, "html.parser")
    media_elements = media_source.find_all("img")
    media_urls = [media["src"] for media in media_elements]
    return choice(media_urls)


def _get_random_source() -> str:
    with open(_MEDIA_SOURCES_FILE) as sources_file:
        sources = safe_load(sources_file)
    source_name, source_url = choice(list(sources.items()))
    _logger.info(f"Using [{source_name}] [{source_url}]")
    return source_url