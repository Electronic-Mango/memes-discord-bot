"""
Command Cog sending back a random pasta.
Output language can be configured with dedicated command.
"""

from logging import getLogger

from discord.ext.commands import Cog, Context, command
from discord.utils import escape_markdown
from more_itertools import sliced

from resources import get_pasta
from settings import BOT_DEEP_FRIED_LANGUAGE, BOT_MAX_TEXT_MESSAGE_LENGTH
from translator import detect_language, is_valid_language, translate


class Pasta(Cog, name="Get a random pasta"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)
        self._languages = dict()

    @command(name="pasta")
    async def pasta(self, context: Context) -> None:
        """Get a random pasta"""
        pasta = get_pasta()
        if context.channel.id in self._languages:
            pasta = translate(pasta, self._languages[context.channel.id])
        await self._send_pasta(context, pasta)

    @command(name="setlanguage", aliases=["lang", "language"])
    async def set_language(self, context: Context, *, target_language: str) -> None:
        """Set language for "pasta" command output"""
        if not is_valid_language(target_language):
            await context.reply(f"{target_language} is not valid")
        else:
            self._languages[context.channel.id] = target_language
            await context.reply(f"Set language to **{target_language}**")

    @command(name="resetlanguage", aliases=["resetlang"])
    async def reset_language(self, context: Context) -> None:
        """Reset language for "pasta" command output"""
        self._languages.pop(context.channel.id, None)
        await context.reply("Set language to default")

    @command(name="deepfriedpasta", aliases=["dfpasta", "dfp"])
    async def deep_fried_pasta(self, context: Context) -> None:
        """Get a random deep-fried-pasta"""
        pasta = get_pasta()
        original_language = detect_language(pasta)
        pasta = translate(pasta, BOT_DEEP_FRIED_LANGUAGE)
        target_language = self._languages.get(context.channel.id, original_language)
        pasta = translate(pasta, target_language)
        await self._send_pasta(context, pasta)

    async def _send_pasta(self, context: Context, pasta: str) -> None:
        sliced_pasta = sliced(escape_markdown(pasta), BOT_MAX_TEXT_MESSAGE_LENGTH)
        sliced_pasta = [slice.strip() for slice in sliced_pasta]
        for slice in sliced_pasta:
            await context.reply(slice)
