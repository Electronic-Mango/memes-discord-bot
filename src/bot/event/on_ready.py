"""
Event Cog logging information that bot is ready.
"""

from logging import getLogger

from disnake.ext.commands import Bot, Cog

from bot.command.media import MediaCog


class OnReady(Cog):
    def __init__(self, bot: Bot, periodic_media_cog: MediaCog) -> None:
        self._bot = bot
        self._periodic_media_cog = periodic_media_cog
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_ready(self) -> None:
        self._logger.info(f"[{self._bot.user}] ready, initializing periodic media")
        self._periodic_media_cog.initialize_periodic_tasks()
