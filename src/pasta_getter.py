from logging import getLogger
from os import getenv
from random import choice

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from feedparser import parse

load_dotenv()
_PASTA_RSS_SOURCE = getenv("PASTA_RSS_SOURCE")

_logger = getLogger(__name__)


def get_pasta() -> tuple[str, bool]:
    feed = parse(_PASTA_RSS_SOURCE)
    random_item = choice(feed.entries)
    _logger.info(f"Using [{random_item.link}] for source")
    pasta_source = BeautifulSoup(random_item.summary, "html.parser")
    return pasta_source.find("p").getText().strip()
