"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from asyncio import sleep
from io import BytesIO
from logging import getLogger
from sys import getsizeof
from typing import Callable

from aiohttp import ClientSession
from asyncio import AbstractEventLoop
from disnake import CommandInteraction, File
from disnake.ext.commands import Cog, Param, slash_command

from resources import get_random_media_url
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_GROUP = BOT_COMMANDS["media_group"]
_MEDIA_GROUP_NAME = _MEDIA_GROUP["name"]

_GET = _MEDIA_GROUP["commands"]["get"]
_GET_NAME = _GET.get("name")
_GET_DESCRIPTION = _GET.get("description")

# TODO: Change interval unit from "seconds" to "minutes"
# TODO: Move these to settings YAML
_PERIODIC_GROUP_NAME = "periodic"

_PERIODIC_ENABLE_NAME = "enable"
_PERIODIC_ENABLE_DESCRIPTION = "Enable periodic media"
_PERIODIC_INTERVAL_PARAMETER_HINT = "How often media should be sent in seconds"

_PERIODIC_DISABLE_NAME = "disable"
_PERIODIC_DISABLE_DESCRIPTION = "Disable periodic media"

HELP_MESSAGE = f"""
`/{_MEDIA_GROUP_NAME} {_GET_NAME}` - {_GET_DESCRIPTION}
"""


class MediaCog(Cog):
    def __init__(self, event_loop: AbstractEventLoop) -> None:
        self._loop = event_loop
        self._logger = getLogger(__name__)
        self._periodic_channels = dict()

    @slash_command(name=_MEDIA_GROUP_NAME)
    async def media(self, _: CommandInteraction) -> None:
        pass

    @media.sub_command(name=_GET_NAME, description=_GET_DESCRIPTION)
    async def get_media(self, interaction: CommandInteraction) -> None:
        """Get a random media"""
        await interaction.response.defer()
        await self._handle_new_media(interaction.send)

    @media.sub_command_group(name=_PERIODIC_GROUP_NAME)
    async def periodic(self, _: CommandInteraction) -> None:
        pass

    @periodic.sub_command(name=_PERIODIC_ENABLE_NAME, description=_PERIODIC_ENABLE_DESCRIPTION)
    async def periodic_enable(
        self,
        interaction: CommandInteraction,
        interval: int = Param(description=_PERIODIC_INTERVAL_PARAMETER_HINT),
    ) -> None:
        channel = interaction.channel
        channel_id = channel.id
        self._stop_periodic_media(channel_id)
        periodic_media_task = self._loop.create_task(self._periodic_media(channel, interval))
        self._periodic_channels[channel_id] = periodic_media_task
        self._logger.info(f"[{channel_id}] Sending periodic media every {interval} seconds")
        await interaction.send(f"Sending periodic media every {interval} seconds")
        await periodic_media_task

    @periodic.sub_command(name=_PERIODIC_DISABLE_NAME, description=_PERIODIC_DISABLE_DESCRIPTION)
    async def periodic_disable(self, interaction: CommandInteraction) -> None:
        channel_id = interaction.channel_id
        self._stop_periodic_media(channel_id)
        self._logger.info(f"[{channel_id}] Stopping periodic media")
        await interaction.send("Stopping periodic media")

    def _stop_periodic_media(self, channel_id: int) -> None:
        if channel_id in self._periodic_channels:
            self._periodic_channels.pop(channel_id).cancel()

    async def _periodic_media(self, channel, interval: int) -> None:
        while not await sleep(interval):
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
