"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from aiohttp import ClientSession
from logging import getLogger
from io import BytesIO
from sys import getsizeof

from discord import File
from discord.ext.commands import Cog, Context, command

from resources import get_random_media_url
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_COMMAND_NAMES = BOT_COMMANDS["media"]


class Media(Cog, name="Send back a random media (image, GIFs, videos, etc.)"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @command(name=_MEDIA_COMMAND_NAMES[0], aliases=_MEDIA_COMMAND_NAMES[1:])
    async def media(self, context: Context) -> None:
        """Get a random media"""
        media, url = await self._get_media()
        while getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{getsizeof(media)}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
            media, url = await self._get_media()
        await context.send(file=File(media, url.split("/")[-1]))

    async def _get_media(self) -> tuple[bytes, str]:
        media_url = get_random_media_url()
        media_bytes = await self._download_media(media_url)
        self._logger.info(f"Trying to send [{media_url}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, media_url

    async def _download_media(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())
