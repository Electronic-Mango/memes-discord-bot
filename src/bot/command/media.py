"""
Command Cog sending back a random media (image, GIFs, videos, etc.).
"""

from asyncio import sleep
from datetime import datetime
from io import BytesIO
from logging import getLogger
from os.path import splitext
from re import fullmatch
from sys import getsizeof
from typing import Callable

from aiohttp import ClientSession
from disnake import Client, CommandInteraction, File
from disnake.ext.commands import Cog, Param, slash_command

from db.client import get_all_periodic_media_data, remove_interval, store_interval
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

_PERIODIC_LIST = _PERIODIC_SUBGROUP["list"]
_PERIODIC_LIST_NAME = _PERIODIC_LIST.get("name")
_PERIODIC_LIST_DESCRIPTION = _PERIODIC_LIST.get("description")

HELP_MESSAGE = f"""
`/{_MEDIA_GROUP_NAME} {_GET_NAME}` - {_GET_DESCRIPTION}
`/{_MEDIA_GROUP_NAME} {_PERIODIC_SUBGROUP_NAME} {_PERIODIC_ENABLE_NAME} <interval>`\
 - {_PERIODIC_ENABLE_DESCRIPTION}
`/{_MEDIA_GROUP_NAME} {_PERIODIC_SUBGROUP_NAME} {_PERIODIC_DISABLE_NAME}`\
 - {_PERIODIC_DISABLE_DESCRIPTION}
`/{_MEDIA_GROUP_NAME} {_PERIODIC_SUBGROUP_NAME} {_PERIODIC_LIST_NAME}`\
 - {_PERIODIC_LIST_DESCRIPTION}
"""

_INVALID_FILENAME_PATTERN = r"[./\\]+"
_DEFAULT_FILENAME = "file"


class MediaCog(Cog):
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._logger = getLogger(__name__)
        self._periodic_channels = dict()

    def initialize_periodic_tasks(self) -> None:
        if self._periodic_channels:
            self._logger.warning("Periodic media already initialized!")
            return
        for channel_id, interval in get_all_periodic_media_data():
            channel = self._bot.get_channel(channel_id)
            self._create_periodic_media_task(channel, interval)

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
        self._stop_periodic_media(channel.id)
        self._create_periodic_media_task(channel, interval)
        store_interval(channel.id, interval)
        await interaction.send(f"Sending periodic media every {interval} minutes")

    @periodic.sub_command(name=_PERIODIC_DISABLE_NAME, description=_PERIODIC_DISABLE_DESCRIPTION)
    async def periodic_disable(self, interaction: CommandInteraction) -> None:
        channel_id = interaction.channel_id
        self._stop_periodic_media(channel_id)
        remove_interval(channel_id)
        self._logger.info(f"[{channel_id}] Stopping periodic media")
        await interaction.send("Stopping periodic media")

    @periodic.sub_command(name=_PERIODIC_LIST_NAME, description=_PERIODIC_LIST_DESCRIPTION)
    async def periodic_list(self, interaction: CommandInteraction) -> None:
        if not self._periodic_channels:
            await interaction.send("No periodic media enabled", ephemeral=True)
            return
        channels = [self._bot.get_channel(id) for id in self._periodic_channels.keys()]
        message = "Sending media to:\n"
        message += "\n".join(f"- {channel.guild} - **{channel.name}**" for channel in channels)
        await interaction.send(message, ephemeral=True)

    def _stop_periodic_media(self, channel_id: int) -> None:
        if channel_id in self._periodic_channels:
            self._periodic_channels.pop(channel_id).cancel()

    def _create_periodic_media_task(self, channel, interval: int) -> None:
        periodic_media_task = self._bot.loop.create_task(self._periodic_media(channel, interval))
        self._periodic_channels[channel.id] = periodic_media_task
        self._logger.info(f"[{channel.id}] Sending periodic media every {interval} minutes")

    async def _periodic_media(self, channel, interval_minutes: int) -> None:
        while not await sleep(interval_minutes * 60):
            if datetime.now().hour in _PERIODIC_QUIET_HOURS:
                self._logger.info(f"[{channel.id}] Quiet hour, skipping transmission")
                continue
            self._logger.info(f"[{channel.id}] Sending periodic media")
            self._bot.loop.create_task(self._handle_new_media(channel.send))

    async def _handle_new_media(self, sender: Callable) -> None:
        media, url, title = await self._get_media()
        while size := getsizeof(media) > BOT_MAX_FILESIZE_BYTES:
            self._logger.info(f"[{url}] [{title}] [{size}] exceeds [{BOT_MAX_FILESIZE_BYTES}]")
            media, url, title = await self._get_media()
        url_filename, extension = splitext(url)
        url_filename = url_filename.split("/")[-1]
        filename = f"{self._select_filename(title, url_filename)}{extension}"
        await sender(file=File(media, filename))

    async def _get_media(self) -> tuple[BytesIO, str, str]:
        url, title = await get_random_media_url_and_title()
        media_bytes = await self._download_media(url)
        self._logger.info(f"Trying to send [{url}] [{title}] [{getsizeof(media_bytes)}] bytes")
        return media_bytes, url, title

    async def _download_media(self, url: str) -> BytesIO:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return BytesIO(await response.read())

    def _select_filename(self, title: str, url_filename: str) -> str:
        if self._filename_is_valid(title):
            return title
        elif self._filename_is_valid(url_filename):
            return url_filename
        else:
            return _DEFAULT_FILENAME

    def _filename_is_valid(self, filename: str) -> bool:
        return filename is not None and not fullmatch(_INVALID_FILENAME_PATTERN, filename)
