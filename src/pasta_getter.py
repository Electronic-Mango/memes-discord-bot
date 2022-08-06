from os import getenv

from dotenv import load_dotenv
from requests import get

load_dotenv()
_PASTA_API_SOURCE = getenv("PASTA_API_SOURCE")


def get_pasta() -> str:
    item = get(_PASTA_API_SOURCE).json()
    return item["selftext"].strip()
