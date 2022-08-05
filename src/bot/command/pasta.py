"""
Command Cog sending back a random pasta.
"""

from os import getenv
from logging import getLogger

from discord.ext.commands import Cog, Context, command
from dotenv import load_dotenv
from more_itertools import sliced

from pasta_getter import get_pasta
from translator import translate

load_dotenv
_MAX_TEXT_MESSAGE_LENGTH = int(getenv("MAX_TEXT_MESSAGE_LENGTH"))
_TARGET_LANGUAGE = getenv("TARGET_LANGUAGE")


class Pasta(Cog, name="Get a random pasta"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @command(name="pasta")
    async def pasta(self, context: Context) -> None:
        """Get a random pasta"""
        pasta = get_pasta()
        pasta = translate(pasta, _TARGET_LANGUAGE)
        sliced_pasta = sliced(pasta, _MAX_TEXT_MESSAGE_LENGTH)
        for slice in sliced_pasta:
            await context.reply(slice)
