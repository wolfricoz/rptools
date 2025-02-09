import json
import random
from abc import ABC, abstractmethod

import discord


# noinspection PyMethodParameters
class Templater(ABC):
    @abstractmethod
    @staticmethod
    async def apply(interaction: discord.interactions, archive: discord.CategoryChannel, data):
        categories = [category for category in interaction.guild.categories if not category.name.startswith("archived")]
        channels = [channel for category in categories for channel in category.channels]
        for c in channels:
            if len(archive.channels) >= 49:
                archive = await interaction.guild.create_category(name=f"archive-overflow")
            print(f"removing {c}")
            await c.edit(category=archive, name=f"archived-{c}", )
            await c.set_permissions(interaction.guild.default_role, read_messages=False)
        for category in categories:
            await category.delete(reason=f"Template being applied")
        for item in data:
            cat = await interaction.guild.create_category(name=f"{item}")
            for i in data[item]:
                print(f"channel {i}")
                await interaction.guild.create_text_channel(name=f"{i}", category=cat)


# noinspection PyMethodParameters
class Gen(ABC):
    @abstractmethod
    async def name(gtype, amount):
        with open(f'tools/{gtype}names.json', 'r') as f:
            data = json.load(f)
            x = 0
            names = []
            while x < amount:
                r = random.randint(0, len(data['names']))
                names.append(data['names'][r])
                x += 1
            return names
