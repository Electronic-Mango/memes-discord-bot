"""
Command Cog sending back a random pasta.
Output language can be configured with dedicated command.
"""

from os import getenv
from logging import getLogger

from discord.ext.commands import Cog, Context, command
from dotenv import load_dotenv
from more_itertools import sliced

from pasta_getter import get_pasta
from translator import is_valid_language, translate

load_dotenv
_MAX_TEXT_MESSAGE_LENGTH = int(getenv("MAX_TEXT_MESSAGE_LENGTH"))


class Pasta(Cog, name="Get a random pasta"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)
        self._language = None

    @command(name="pasta")
    async def pasta(self, context: Context) -> None:
        """Get a random pasta"""
        pasta = get_pasta()
        if self._language:
            pasta = translate(pasta, self._language)
        sliced_pasta = sliced(pasta, _MAX_TEXT_MESSAGE_LENGTH)
        for slice in sliced_pasta:
            await context.reply(slice)
    
    @command(name="setlanguage", aliases=["lang", "language"])
    async def set_language(self, context: Context, *, target_language: str) -> None:
        """Set language for "pasta" command output"""
        if not is_valid_language(target_language):
            await context.reply(f"{target_language} is not valid")
        else:
            self._language = target_language
            await context.reply(f"Set language to **{target_language}**")
    
    @command(name="resetlanguage", aliases=["resetlang"])
    async def reset_language(self, context: Context) -> None:
        """Reset language for "pasta" command output"""
        self._language = None
        await context.reply("Set language to default")
