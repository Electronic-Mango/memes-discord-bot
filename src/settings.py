from functools import reduce
from dotenv import load_dotenv
from os import getenv
from typing import Any

from yaml import safe_load

load_dotenv()

_DEFAULT_SETTINGS_YAML_PATH = "settings.yml"
_SETTINGS_YAML_PATH = getenv("SETTINGS_YAML_PATH", _DEFAULT_SETTINGS_YAML_PATH)
with open(_SETTINGS_YAML_PATH) as settings_yaml:
    _SETTINGS_YAML = safe_load(settings_yaml)


def _load_config(*keys: tuple[str]) -> Any:
    return reduce(lambda table, key: table[key], keys, _SETTINGS_YAML)


BOT_TOKEN = _load_config("bot", "token")
BOT_COMMAND_PREFIX = _load_config("bot", "command_prefix")
BOT_MAX_FILESIZE_BYTES = _load_config("bot", "max_filesize_bytes")
BOT_MAX_TEXT_MESSAGE_LENGTH = _load_config("bot", "max_text_message_length")
BOT_DEEP_FRIED_LANGUAGE = _load_config("bot", "deep_fried_language")

SOURCES_FILE = _load_config("sources", "file")
