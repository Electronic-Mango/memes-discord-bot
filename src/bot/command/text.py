"""
Command Cog sending back a random text.
Output language can be configured with dedicated command.
"""

from functools import reduce

from discord import ApplicationContext, SlashCommandGroup
from discord.utils import escape_markdown
from more_itertools import sliced

from resources import get_random_text
from settings import BOT_COMMANDS, BOT_DEEP_FRIED_LANGUAGES, BOT_MAX_TEXT_MESSAGE_LENGTH
from translator import is_valid_language, translate

_COMMAND = BOT_COMMANDS["text"]
_COMMAND_GROUP_NAME = _COMMAND["group"]["group_name"]
_COMMAND_DESCRIPTION = _COMMAND["group"]["description"]
_GET_COMMAND = _COMMAND["commands"]["get"]
_SET_LANGUAGE = _COMMAND["commands"]["set_language"]
_RESET_LANGUAGE = _COMMAND["commands"]["reset_language"]
_DEEP_FRY_TEXT = _COMMAND["commands"]["deep_fry_text"]

_languages = dict()

text_command_group = SlashCommandGroup(_COMMAND_GROUP_NAME, _COMMAND_DESCRIPTION)
_command = text_command_group.command


@_command(name=_GET_COMMAND["name"], description=_GET_COMMAND["description"])
async def text(context: ApplicationContext) -> None:
    """Get a random text message"""
    await context.defer()
    text, _ = get_random_text()
    if context.channel.id in _languages:
        text = translate(text, _languages[context.channel.id])
    await _send_text(context, text)


@_command(name=_SET_LANGUAGE["name"], description=_SET_LANGUAGE["description"])
async def set_language(context: ApplicationContext, *, target_language: str) -> None:
    """Set language for text-based commands output"""
    if is_valid_language(target_language):
        _languages[context.channel.id] = target_language
        await context.respond(f"Set language to **{target_language}**")
    else:
        await context.respond(f"**{target_language}** isn't a valid language")


@_command(name=_RESET_LANGUAGE["name"], description=_RESET_LANGUAGE["description"])
async def reset_language(context: ApplicationContext) -> None:
    """Reset language for text-based commands output"""
    _languages.pop(context.channel.id, None)
    await context.respond("Set language to default")


@_command(name=_DEEP_FRY_TEXT["name"], description=_DEEP_FRY_TEXT["description"])
async def deep_fried_text(context: ApplicationContext) -> None:
    """Get a random deep-fried text"""
    await context.defer()
    text, original_language = get_random_text()
    target_language = _languages.get(context.channel.id, original_language)
    deep_fried_text = reduce(translate, BOT_DEEP_FRIED_LANGUAGES + [target_language], text)
    await _send_text(context, deep_fried_text)


async def _send_text(context: ApplicationContext, text: str) -> None:
    sliced_text = sliced(escape_markdown(text), BOT_MAX_TEXT_MESSAGE_LENGTH)
    for slice in sliced_text:
        await context.respond(slice.strip())
