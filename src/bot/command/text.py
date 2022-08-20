"""
Command Cog sending back a random text.
Output language can be configured with dedicated command.
"""

from asyncstdlib import reduce
from disnake import CommandInteraction
from disnake.ext.commands import Cog, Param, slash_command
from disnake.utils import escape_markdown
from more_itertools import sliced

from db.wrapper import get_language, remove_language, store_language
from resources import get_random_text
from settings import BOT_COMMANDS, BOT_DEEP_FRIED_LANGUAGES, BOT_MAX_TEXT_MESSAGE_LENGTH
from translator import is_valid_language, supported_languages_matches, translate

_MAX_AUTOCOMPLETION_SIZE = 25

_TEXT_GROUP = BOT_COMMANDS["text_group"]
_TEXT_GROUP_NAME = _TEXT_GROUP["name"]

_GET = _TEXT_GROUP["commands"]["get"]
_GET_NAME = _GET.get("name")
_GET_DESCRIPTION = _GET.get("description")

_DEEP_FRY_TEXT = _TEXT_GROUP["commands"]["deep_fry_text"]
_DEEP_FRY_TEXT_NAME = _DEEP_FRY_TEXT.get("name")
_DEEP_FRY_TEXT_DESCRIPTION = _DEEP_FRY_TEXT.get("description")

_LANG_SUBGROUP = _TEXT_GROUP["language_subgroup"]
_LANG_SUBGROUP_NAME = _LANG_SUBGROUP["name"]

_SET_LANG = _LANG_SUBGROUP["commands"]["set"]
_SET_LANG_NAME = _SET_LANG.get("name")
_SET_LANG_DESCRIPTION = _SET_LANG.get("description")
_SET_LANG_PARAMETER_HINT = _SET_LANG.get("autocomplete_hint")

_RESET_LANG = _LANG_SUBGROUP["commands"]["reset"]
_RESET_LANG_NAME = _RESET_LANG.get("name")
_RESET_LANG_DESCRIPTION = _RESET_LANG.get("description")

HELP_MESSAGE = f"""
`/{_TEXT_GROUP_NAME} {_GET_NAME}` - {_GET_DESCRIPTION}
`/{_TEXT_GROUP_NAME} {_DEEP_FRY_TEXT_NAME}` - {_DEEP_FRY_TEXT_DESCRIPTION}
`/{_TEXT_GROUP_NAME} {_LANG_SUBGROUP_NAME} {_SET_LANG_NAME} <language>` - {_SET_LANG_DESCRIPTION}
`/{_TEXT_GROUP_NAME} {_LANG_SUBGROUP_NAME} {_RESET_LANG_NAME}` - {_RESET_LANG_DESCRIPTION}
"""


class TextCog(Cog):
    @slash_command(name=_TEXT_GROUP_NAME)
    async def text(self, _: CommandInteraction) -> None:
        pass

    @text.sub_command(name=_GET_NAME, description=_GET_DESCRIPTION)
    async def get_text(self, interaction: CommandInteraction) -> None:
        """Get a random text message"""
        await interaction.response.defer()
        text, _ = await get_random_text()
        if language := get_language(interaction.channel.id):
            text = await translate(text, language)
        await self._send_text(interaction, text)

    @text.sub_command(name=_DEEP_FRY_TEXT_NAME, description=_DEEP_FRY_TEXT_DESCRIPTION)
    async def get_deep_fried_text(self, interaction: CommandInteraction) -> None:
        """Get a random deep-fried text"""
        await interaction.response.defer()
        text, original_language = await get_random_text()
        target_lang = get_language(interaction.channel.id) or original_language
        deep_fried_text = await reduce(translate, BOT_DEEP_FRIED_LANGUAGES + [target_lang], text)
        await self._send_text(interaction, deep_fried_text)

    @text.sub_command_group(name=_LANG_SUBGROUP_NAME)
    async def language(self, _: CommandInteraction) -> None:
        pass

    @language.sub_command(name=_SET_LANG_NAME, description=_SET_LANG_DESCRIPTION)
    async def set_language(
        self,
        interaction: CommandInteraction,
        language: str = Param(
            description=_SET_LANG_PARAMETER_HINT,
            converter=lambda _, input: input.lower(),
        ),
    ) -> None:
        """Set language for text-based commands output"""
        await interaction.response.defer()
        if is_valid_language(language):
            store_language(interaction.channel.id, language)
            await interaction.send(f"Set language to **{language}**")
        else:
            await interaction.send(f"**{language}** isn't a valid language")

    @set_language.autocomplete("language")
    async def _get_languages(self, _: CommandInteraction, input: str) -> list[str]:
        return supported_languages_matches(input)[:_MAX_AUTOCOMPLETION_SIZE]

    @language.sub_command(name=_RESET_LANG_NAME, description=_RESET_LANG_DESCRIPTION)
    async def reset_language(self, interaction: CommandInteraction) -> None:
        """Reset language for text-based commands output"""
        await interaction.response.defer()
        remove_language(interaction.channel.id)
        await interaction.send("Set language to default")

    async def _send_text(self, interaction: CommandInteraction, text: str) -> None:
        sliced_text = sliced(escape_markdown(text), BOT_MAX_TEXT_MESSAGE_LENGTH)
        for slice in sliced_text:
            await interaction.send(slice.strip())
