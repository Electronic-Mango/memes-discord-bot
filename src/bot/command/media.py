"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from io import BytesIO
from logging import getLogger
from sys import getsizeof
from typing import Callable

from aiohttp import ClientSession
from disnake import CommandInteraction, File
from disnake.ext import tasks
from disnake.ext.commands import Cog, slash_command

from resources import get_random_media_url
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_GROUP = BOT_COMMANDS["media_group"]
_MEDIA_GROUP_NAME = _MEDIA_GROUP["name"]

_GET = _MEDIA_GROUP["commands"]["get"]
_GET_NAME = _GET.get("name")
_GET_DESCRIPTION = _GET.get("description")

# TODO: Move these to settings YAML
_PERIODIC_NAME = "periodic"
_PERIODIC_DESCRIPTION = "Toggle periodic media"
_PERIODIC_PERIOD_SECONDS = 15

HELP_MESSAGE = f"""
`/{_MEDIA_GROUP_NAME} {_GET_NAME}` - {_GET_DESCRIPTION}
"""


class MediaCog(Cog):
    def __init__(self) -> None:
        self._logger = getLogger(__name__)
        self._periodic_channels = set()
        self._periodic_media.start()

    @slash_command(name=_MEDIA_GROUP_NAME)
    async def media(self, _: CommandInteraction) -> None:
        pass

    @media.sub_command(name=_GET_NAME, description=_GET_DESCRIPTION)
    async def get_media(self, interaction: CommandInteraction) -> None:
        """Get a random media"""
        await interaction.response.defer()
        await self._handle_new_media(interaction.send)

    @media.sub_command(name=_PERIODIC_NAME, description=_PERIODIC_DESCRIPTION)
    async def periodic_media(self, interaction: CommandInteraction) -> None:
        if (channel := interaction.channel) in self._periodic_channels:
            self._periodic_channels.remove(channel)
            self._logger.info(f"[{channel.id}] Channel added for periodic media")
            await interaction.send("Channel removed")
        else:
            self._periodic_channels.add(channel)
            self._logger.info(f"[{channel.id}] Channel removed from periodic media")
            await interaction.send("Channel added")

    @tasks.loop(seconds=_PERIODIC_PERIOD_SECONDS)
    async def _periodic_media(self):
        self._logger.info("Triggering periodic media transmissions")
        for channel in self._periodic_channels:
            self._logger.info(f"[{channel.id}] Sending periodic media")
            await self._handle_new_media(channel.send)

    async def _handle_new_media(self, sender: Callable) -> None:
        media, url = await self._get_media()
        while getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{getsizeof(media)}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
            media, url = await self._get_media()
        await sender(file=File(media, url.split("/")[-1]))

    async def _get_media(self) -> tuple[bytes, str]:
        media_url = await get_random_media_url()
        media_bytes = await self._download_media(media_url)
        self._logger.info(f"Trying to send [{media_url}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, media_url

    async def _download_media(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())
