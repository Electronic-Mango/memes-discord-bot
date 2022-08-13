"""
Command Cog sending back a random text.
Output language can be configured with dedicated command.
"""

from functools import reduce

from discord.ext.commands import Cog, Context, command
from discord.utils import escape_markdown
from more_itertools import sliced

from resources import get_random_text
from settings import BOT_COMMANDS, BOT_DEEP_FRIED_LANGUAGES, BOT_MAX_TEXT_MESSAGE_LENGTH
from translator import is_valid_language, translate

_TEXT_COMMAND_NAMES = BOT_COMMANDS["text"]
_SET_LANGUAGE_COMMAND_NAMES = BOT_COMMANDS["set_language"]
_RESET_LANGUAGE_COMMAND_NAMES = BOT_COMMANDS["reset_language"]
_DEEP_FRIED_TEXT_COMMAND_NAMES = BOT_COMMANDS["deep_fried_text"]


class Text(Cog, name="Get a random text"):
    def __init__(self) -> None:
        self._languages = dict()

    @command(name=_TEXT_COMMAND_NAMES[0], aliases=_TEXT_COMMAND_NAMES[1:])
    async def text(self, context: Context) -> None:
        """Get a random text message"""
        text, _ = get_random_text()
        if context.channel.id in self._languages:
            text = translate(text, self._languages[context.channel.id])
        await self._send_text(context, text)

    @command(name=_SET_LANGUAGE_COMMAND_NAMES[0], aliases=_SET_LANGUAGE_COMMAND_NAMES[1:])
    async def set_language(self, context: Context, *, target_language: str) -> None:
        """Set language for text-based commands output"""
        if is_valid_language(target_language):
            self._languages[context.channel.id] = target_language
            await context.send(f"Set language to **{target_language}**")
        else:
            await context.send(f"**{target_language}** isn't a valid language")

    @command(name=_RESET_LANGUAGE_COMMAND_NAMES[0], aliases=_RESET_LANGUAGE_COMMAND_NAMES[1:])
    async def reset_language(self, context: Context) -> None:
        """Reset language for text-based commands output"""
        self._languages.pop(context.channel.id, None)
        await context.send("Set language to default")

    @command(name=_DEEP_FRIED_TEXT_COMMAND_NAMES[0], aliases=_DEEP_FRIED_TEXT_COMMAND_NAMES[1:])
    async def deep_fried_text(self, context: Context) -> None:
        """Get a random deep-fried text"""
        text, original_language = get_random_text()
        target_language = self._languages.get(context.channel.id, original_language)
        deep_fried_text = reduce(translate, BOT_DEEP_FRIED_LANGUAGES + [target_language], text)
        await self._send_text(context, deep_fried_text)

    async def _send_text(self, context: Context, text: str) -> None:
        sliced_text = sliced(escape_markdown(text), BOT_MAX_TEXT_MESSAGE_LENGTH)
        for slice in sliced_text:
            await context.send(slice.strip())
