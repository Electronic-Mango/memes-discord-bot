"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from io import BytesIO
from logging import getLogger
from sys import getsizeof

from aiohttp import ClientSession
from disnake import CommandInteraction, File
from disnake.ext.commands import Cog, slash_command

from resources import get_random_media_url
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_GROUP = BOT_COMMANDS["media_group"]
_MEDIA_GROUP_NAME = _MEDIA_GROUP["name"]
_MEDIA_GROUP_DESCRIPTION = _MEDIA_GROUP.get("description")

_GET = _MEDIA_GROUP["commands"]["get"]
_GET_NAME = _GET.get("name")
_GET_DESCRIPTION = _GET.get("description")


class MediaCog(Cog):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)

    @slash_command(name=_MEDIA_GROUP_NAME, description=_MEDIA_GROUP_DESCRIPTION)
    async def media(self, _: CommandInteraction) -> None:
        pass

    @media.sub_command(name=_GET_NAME, description=_GET_DESCRIPTION)
    async def get_media(self, interaction: CommandInteraction) -> None:
        """Get a random media"""
        await interaction.response.defer()
        media, url = await self._get_media()
        while getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{getsizeof(media)}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
            media, url = await self._get_media()
        await interaction.send(file=File(media, url.split("/")[-1]))

    async def _get_media(self) -> tuple[bytes, str]:
        media_url = await get_random_media_url()
        media_bytes = await self._download_media(media_url)
        self._logger.info(f"Trying to send [{media_url}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, media_url

    async def _download_media(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())
