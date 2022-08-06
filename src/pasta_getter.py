from os import getenv

from dotenv import load_dotenv
from requests import get

load_dotenv()
_PASTA_API_SOURCE = getenv("PASTA_API_SOURCE")
_PASTA_API_TEXT_KEY = getenv("PASTA_API_TEXT_KEY")


def get_pasta() -> str:
    item = get(_PASTA_API_SOURCE).json()
    return item[_PASTA_API_TEXT_KEY].strip()
