import json
import random
from abc import ABC, abstractmethod


# noinspection PyMethodParameters
class Templater(ABC):
    @abstractmethod
    async def apply(interaction, archive, data):
        for c in interaction.guild.text_channels:
            if c.category is archive:
                print(f"passing {c}")
            else:
                print(f"removing {c}")
                await c.edit(category=archive, name=f"archived-{c}", )
                await c.set_permissions(interaction.guild.default_role, read_messages=False)
        for a in interaction.guild.categories:
            if a is archive:
                pass
            else:
                await a.delete(reason=f"empty command used by {interaction.user}")
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
