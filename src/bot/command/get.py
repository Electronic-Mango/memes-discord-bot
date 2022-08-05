"""
Command Cog sending back a random meme.
"""

from os import getenv
from aiohttp import ClientSession
from io import BytesIO
from logging import getLogger
from mimetypes import MimeTypes
from sys import getsizeof

from discord import File
from discord.ext.commands import Cog, Context, command

from image_getter import get_random_image_url

MAX_FILESIZE_BYTES = int(getenv("MAX_FILESIZE_BYTES"))


class Get(Cog, name="Get a random meme"):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @command(name="get")
    async def get(self, context: Context) -> None:
        """Get a random meme"""
        media, url = await self._get_media()
        while getsizeof(media) > MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{getsizeof(media)}] exceeds max [{MAX_FILESIZE_BYTES}]")
            media, url = await self._get_media()
        await context.reply(file=File(media, url.split("/")[-1]))

    async def _get_media(self) -> tuple[bytes, str]:
        meme_url = get_random_image_url()
        media_bytes = await self._download_media(meme_url)
        self._logger.info(f"Trying to send [{meme_url}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, meme_url

    async def _download_media(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())
