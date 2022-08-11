"""
Command Cog sending back a random text.
Output language can be configured with dedicated command.
"""

from logging import getLogger

from discord.ext.commands import Cog, Context, command
from discord.utils import escape_markdown
from more_itertools import sliced

from resources import get_random_text
from settings import BOT_COMMANDS, BOT_DEEP_FRIED_LANGUAGE, BOT_MAX_TEXT_MESSAGE_LENGTH
from translator import detect_language, is_valid_language, translate

_TEXT_COMMAND_NAMES = BOT_COMMANDS["text"]
_SET_LANGUAGE_COMMAND_NAMES = BOT_COMMANDS["set_language"]
_RESET_LANGUAGE_COMMAND_NAMES = BOT_COMMANDS["reset_language"]
_DEEP_FRIED_TEXT_COMMAND_NAMES = BOT_COMMANDS["deep_fried_text"]


class Text(Cog, name="Get a random text"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)
        self._languages = dict()

    @command(name=_TEXT_COMMAND_NAMES[0], aliases=_TEXT_COMMAND_NAMES[1:])
    async def text(self, context: Context) -> None:
        """Get a random text message"""
        text = get_random_text()
        if context.channel.id in self._languages:
            text = translate(text, self._languages[context.channel.id])
        await self._send_text(context, text)

    @command(name=_SET_LANGUAGE_COMMAND_NAMES[0], aliases=_SET_LANGUAGE_COMMAND_NAMES[1:])
    async def set_language(self, context: Context, *, target_language: str) -> None:
        """Set language for text-based commands output"""
        if not is_valid_language(target_language):
            await context.reply(f"{target_language} is not valid")
        else:
            self._languages[context.channel.id] = target_language
            await context.reply(f"Set language to **{target_language}**")

    @command(name=_RESET_LANGUAGE_COMMAND_NAMES[0], aliases=_RESET_LANGUAGE_COMMAND_NAMES[1:])
    async def reset_language(self, context: Context) -> None:
        """Reset language for text-based commands output"""
        self._languages.pop(context.channel.id, None)
        await context.reply("Set language to default")

    @command(name=_DEEP_FRIED_TEXT_COMMAND_NAMES[0], aliases=_DEEP_FRIED_TEXT_COMMAND_NAMES[1:])
    async def deep_fried_text(self, context: Context) -> None:
        """Get a random deep-fried text"""
        text = get_random_text()
        original_language = detect_language(text)
        text = translate(text, BOT_DEEP_FRIED_LANGUAGE)
        target_language = self._languages.get(context.channel.id, original_language)
        text = translate(text, target_language)
        await self._send_text(context, text)

    async def _send_text(self, context: Context, text: str) -> None:
        sliced_text = sliced(escape_markdown(text), BOT_MAX_TEXT_MESSAGE_LENGTH)
        sliced_text = [slice.strip() for slice in sliced_text]
        for slice in sliced_text:
            await context.reply(slice)
