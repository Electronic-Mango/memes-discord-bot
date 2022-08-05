from os import getenv
from random import choice

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from feedparser import parse

load_dotenv()
IMAGES_RSS_FEED = getenv("IMAGES_RSS_FEED")


def get_random_image_url() -> str:
    feed = parse(IMAGES_RSS_FEED)
    feed_items = list(feed.entries)
    random_item = choice(feed_items)
    media_source = BeautifulSoup(random_item.summary, "html.parser")
    media_elements = media_source.find_all("img")
    media_sources = [media["src"] for media in media_elements]
    return choice(media_sources)
