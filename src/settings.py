from functools import reduce
from dotenv import load_dotenv
from os import getenv
from typing import Any

from mergedeep import merge
from yaml import safe_load

load_dotenv()
_DEFAULT_SETTINGS_PATH = "settings.yml"
_CUSTOM_SETTINGS_PATH_VARIABLE_NAME = "CUSTOM_SETTINGS_PATH"
_CUSTOM_SETTINGS_PATH = getenv(_CUSTOM_SETTINGS_PATH_VARIABLE_NAME)


def _load_settings(settings_path: str) -> dict[str, Any]:
    with open(settings_path) as settings_yaml:
        return safe_load(settings_yaml)


_SETTINGS = merge(
    _load_settings(_DEFAULT_SETTINGS_PATH),
    _load_settings(_CUSTOM_SETTINGS_PATH) if _CUSTOM_SETTINGS_PATH else {},
)


def _load_config(*keys: tuple[str]) -> Any:
    return reduce(lambda table, key: table[key], keys, _SETTINGS)


BOT_TOKEN = _load_config("bot", "token")
BOT_COMMAND_PREFIX = _load_config("bot", "command_prefix")
BOT_MAX_FILESIZE_BYTES = _load_config("bot", "max_filesize_bytes")
BOT_MAX_TEXT_MESSAGE_LENGTH = _load_config("bot", "max_text_message_length")
BOT_DEEP_FRIED_LANGUAGE = _load_config("bot", "deep_fried_language")
BOT_COMMANDS = _load_config("bot", "commands")

SOURCES_FILE = _load_config("sources", "file")
