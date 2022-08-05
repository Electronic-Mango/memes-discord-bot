"""
Event Cog logging information that bot is ready to internal logger.
"""

from logging import getLogger

from discord.ext.commands import Bot, Cog


class OnReady(Cog):
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._logger = getLogger(__name__)

    @Cog.listener()
    async def on_ready(self) -> None:
        self._logger.info(f"[{self._bot.user}] ready")
