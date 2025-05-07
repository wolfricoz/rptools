import logging

import discord
from discord import app_commands
from discord.ext import commands

from discord_py_utilities.messages import send_response

from models.character import Character


class CharacterCog(commands.GroupCog, name="character"):
    def __init__(self, bot):
        self.bot = bot

    async def characterautocomplete(self, interaction: discord.Interaction, current: str):
        characters = Character().get_all(interaction.user.id)
        return [discord.app_commands.Choice(name=character.name, value=character.id) for character in characters if
                character.name.lower().startswith(current.lower())]

    @app_commands.command(name="create", description="Create a new character")
    async def create(self, interaction: discord.Interaction, name: str, prefix: str):
        if len(name) > 255:
            return await send_response(interaction,"Name can not be longer than 255 characters.")
        if len(prefix) > 255:
            return await send_response(interaction,"Prefix can not be longer than 266 characters.")
        if Character().create(interaction.user.id, name, prefix) is None:
            return await send_response(interaction,"Character already exists.")

        await send_response(interaction,f"Character {name} created with prefix {prefix}")

    @app_commands.command(name="view", description="View your characters")
    @app_commands.autocomplete(character=characterautocomplete)
    async def view(self, interaction: discord.Interaction, character: int):
        character = Character(character)
        logging.info(character.get_all_character_info())
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        embed = discord.Embed(title=character.name, description=f"")
        for k, v in character.character_info.items():
            embed.add_field(name=k, value=v.get("value", ""), inline=False)
        embed.set_footer(text=f"prefix: {character.prefix}")
        return await send_response(interaction, "", embed=embed)

    @app_commands.command(name="delete", description="Delete a character")
    @app_commands.autocomplete(character=characterautocomplete)
    async def delete(self, interaction: discord.Interaction, character: int):
        character = Character(character)
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        character.delete()
        return await send_response(interaction,f"Deleted {character.name}")


    # character info commands

    @app_commands.command(name="add_info", description="Add info to your character")
    @app_commands.autocomplete(character=characterautocomplete)
    async def add_info(self, interaction: discord.Interaction, character: int, key: str, value: str):
        character = Character(character)
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        if len(key) > 255:
            return await send_response(interaction,"Key can not be longer than 255 characters.")
        if len(value) > 1000:
            return await send_response(interaction,"Value can not be longer than 1000 characters.")
        if character.add_character_info(key, value) is None:
            return await send_response(interaction,"Key already exists.")
        return await send_response(interaction,f"Added {key} to {character.name} with value {value}")

    @app_commands.command(name="remove_info", description="Remove info from your character")
    @app_commands.autocomplete(character=characterautocomplete)
    async def remove_info(self, interaction: discord.Interaction, character: int, key: str):
        character = Character(character)
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        if character.remove_character_info(key) is None:
            return await send_response(interaction,"Key does not exist.")
        return await send_response(interaction,f"Removed {key} from {character.name}")

    @app_commands.command(name="edit_info", description="Edit info from your character")
    @app_commands.autocomplete(character=characterautocomplete)
    async def edit_info(self, interaction: discord.Interaction, character: int, key: str, value: str):
        character = Character(character)
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        if len(key) > 255:
            return await send_response(interaction,"Key can not be longer than 255 characters.")
        if len(value) > 1000:
            return await send_response(interaction,"Value can not be longer than 1000 characters.")
        if character.edit_character_info(key, value) is None:
            return await send_response(interaction,"Key does not exist.")
        return await send_response(interaction,f"Edited {key} to {value} in {character.name}")

    @app_commands.command(name="change_info_position", description="Change the position of an info field")
    @app_commands.autocomplete(character=characterautocomplete)
    async def command(self, interaction: discord.Interaction, character: int, key: str, position: int):
        character = Character(character)
        if character.name is None:
            return await send_response(interaction,"Character not found.")
        if character.change_character_info_position(key, position) is None:
            return await send_response(interaction,"Key does not exist.")
        return await send_response(interaction,f"Moved {key} to position {position} in {character.name}")





async def setup(bot):
    await bot.add_cog(CharacterCog(bot))
