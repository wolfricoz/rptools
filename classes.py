import json
import random
from abc import ABC, abstractmethod
from datetime import datetime

import discord
from discord.enums import try_enum
from discord_py_utilities.channels import create_channel


# noinspection PyMethodParameters
class Templater(ABC) :
	@staticmethod
	@abstractmethod
	async def apply(interaction: discord.interactions, archive: discord.CategoryChannel, data) :
		"""Apply the template to the guild"""
		# Cleaning up old channels and categories
		categories = [category for category in interaction.guild.categories if not category.name.lower().startswith("archive")]
		channels = [channel for category in categories for channel in category.channels]
		for c in channels :
			if len(archive.channels) >= 49 :
				archive = await interaction.guild.create_category(name=f"archive-overflow-{datetime.now().strftime('%d-%m-%Y')}")
			await c.edit(category=archive, name=f"archived-{c}", )
			await c.set_permissions(interaction.guild.default_role, read_messages=False)

		# Applying the template
		for category in categories :
			await category.delete(reason=f"Template being applied")
		for item in data :
			cat = await interaction.guild.create_category(name=f"{data[item].get('name')}")
			for i in data[item].get('channels', []) :
				channel_type = try_enum(discord.ChannelType, data[item]["channels"][i].get('type'))
				print(f"{i}: {channel_type}")
				await create_channel(interaction.guild, i, channel_type, category=cat)


# noinspection PyMethodParameters
class Gen(ABC) :
	@staticmethod
	@abstractmethod
	async def name(gtype, amount) :
		with open(f'tools/{gtype}names.json', 'r') as f :
			data = json.load(f)
			x = 0
			names = []
			while x < amount :
				r = random.randint(0, len(data['names']))
				names.append(data['names'][r])
				x += 1
			return names
