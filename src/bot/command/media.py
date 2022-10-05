"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from asyncio import sleep
from io import BytesIO
from logging import getLogger
from os.path import splitext
from sys import getsizeof
from typing import Callable

from aiohttp import ClientSession
from asyncio import AbstractEventLoop
from datetime import datetime
from disnake import CommandInteraction, File
from disnake.ext.commands import Cog, Param, slash_command

from resources import get_random_media_url_and_title
from settings import BOT_COMMANDS, BOT_MAX_FILESIZE_BYTES

_MEDIA_GROUP = BOT_COMMANDS["media_group"]
_MEDIA_GROUP_NAME = _MEDIA_GROUP["name"]

_GET = _MEDIA_GROUP["commands"]["get"]
_GET_NAME = _GET.get("name")
_GET_DESCRIPTION = _GET.get("description")

_PERIODIC_SUBGROUP = _MEDIA_GROUP["commands"]["periodic"]
_PERIODIC_SUBGROUP_NAME = _PERIODIC_SUBGROUP.get("name")
_PERIODIC_QUIET_HOURS = _PERIODIC_SUBGROUP.get("quiet_hours", [])

_PERIODIC_ENABLE = _PERIODIC_SUBGROUP["enable"]
_PERIODIC_ENABLE_NAME = _PERIODIC_ENABLE.get("name")
_PERIODIC_ENABLE_DESCRIPTION = _PERIODIC_ENABLE.get("description")
_PERIODIC_INTERVAL_PARAMETER_HINT = _PERIODIC_ENABLE.get("autocomplete_hint")

_PERIODIC_DISABLE = _PERIODIC_SUBGROUP["disable"]
_PERIODIC_DISABLE_NAME = _PERIODIC_DISABLE.get("name")
_PERIODIC_DISABLE_DESCRIPTION = _PERIODIC_DISABLE.get("description")

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

    @media.sub_command_group(name=_PERIODIC_SUBGROUP_NAME)
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
        self._logger.info(f"[{channel_id}] Sending periodic media every {interval} minutes")
        await interaction.send(f"Sending periodic media every {interval} minutes")

    @periodic.sub_command(name=_PERIODIC_DISABLE_NAME, description=_PERIODIC_DISABLE_DESCRIPTION)
    async def periodic_disable(self, interaction: CommandInteraction) -> None:
        channel_id = interaction.channel_id
        self._stop_periodic_media(channel_id)
        self._logger.info(f"[{channel_id}] Stopping periodic media")
        await interaction.send("Stopping periodic media")

    def _stop_periodic_media(self, channel_id: int) -> None:
        if channel_id in self._periodic_channels:
            self._periodic_channels.pop(channel_id).cancel()

    async def _periodic_media(self, channel, interval_minutes: int) -> None:
        while not await sleep(interval_minutes * 60):
            if datetime.now().hour in _PERIODIC_QUIET_HOURS:
                self._logger.info(f"[{channel.id}] Quiet hour, skipping transmission")
                continue
            self._logger.info(f"[{channel.id}] Sending periodic media")
            await self._handle_new_media(channel.send)

    async def _handle_new_media(self, sender: Callable) -> None:
        media, url, title = await self._get_media()
        while size := getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{title}] [{size}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
            media, url, title = await self._get_media()
        url_filename, extension = splitext(url)
        url_filename = url_filename.split("/")[-1]
        await sender(file=File(media, f"{title or url_filename}{extension}"))

    async def _get_media(self) -> tuple[bytes, str, str]:
        url, title = await get_random_media_url_and_title()
        media_bytes = await self._download_media(url)
        self._logger.info(f"Trying to send [{url}] [{title}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, url, title

    async def _download_media(self, url: str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())
