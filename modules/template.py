import json
import os
from datetime import datetime
from time import sleep
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord_py_utilities.messages import send_response
from sqlalchemy import false

from classes import Templater
from data.globals import MAX_TEMPLATES
from data.messages import NOT_OWNER_ERROR
from database.TemplateTransactions import TemplateTransactions
from views.buttons.confirm import Confirm


# noinspection PyTypeChecker
class Templates(commands.GroupCog, name="template") :
	def __init__(self, bot) :
		self.bot = bot
	cache = {
	}

	async def auto_complete_templates(self, interaction, current: str) :
		if interaction.user.id not in self.cache :
			self.cache[interaction.user.id] = TemplateTransactions().get_all_templates(interaction.user.id)

		return [Choice(name=template, value=template) for template in self.cache[interaction.user.id] if
		        template.lower().startswith(current.lower())]

	@app_commands.command(name="register",
	                      description="Register a template for your server, this will capture the current server state")
	@app_commands.checks.has_permissions(administrator=True)
	async def create_template(self, interaction: discord.Interaction, name: str) -> None :
		# Check how many templates are already registered
		if interaction.user.id in self.cache :
			self.cache.pop(interaction.user.id)
		template_count = TemplateTransactions().count_templates(interaction.user.id)
		if template_count >= MAX_TEMPLATES :
			return await send_response(interaction,
			                           f"You have reached the maximum number of templates ({MAX_TEMPLATES})", ephemeral=True)
		# Check if the user is the owner of the server
		if interaction.user != interaction.guild.owner :
			return await send_response(interaction, NOT_OWNER_ERROR, ephemeral=True)
		data = {

		}
		# Collect the data of the categories and channels, and turns them into a dictionary
		for category in interaction.guild.categories :
			if category.name.lower().startswith("archive") :
				continue
			data[category.id] = {
				"name" : category.name,
				"channels": {}
			}
			for channel in category.channels :
				data[category.id]["channels"][channel.name] = {
					"type" : channel.type.value
				}
		if TemplateTransactions().create_template(interaction.user.id, name, data) is False:
			return await send_response(interaction, f"Template '{name}' already exists", ephemeral=True)
		return await send_response(interaction, f"Template '{name}' created successfully! You can create {MAX_TEMPLATES - TemplateTransactions().count_templates(interaction.user.id)} more templates", ephemeral=True)

	@app_commands.command(name="restore",
	                      description="Applies a template to your server and archives old channels.")
	@app_commands.autocomplete(template=auto_complete_templates)
	@app_commands.checks.has_permissions(administrator=True)
	async def restore_template(self, interaction: discord.Interaction, template: str) :
		# Variables
		template = TemplateTransactions().get_template(interaction.user.id, template)
		archive_name = f"archive-{datetime.now().strftime('%d-%m-%Y')}"
		if template is None:
			return await send_response(interaction, f"Template does not exist", ephemeral=True)
		if interaction.user != interaction.guild.owner :
			return await interaction.followup.send("Only the owner of the server can run this command", ephemeral=True)
		if await Confirm().send_confirm(interaction, f"Are you sure you want to apply the `{template.name}` template?") is False:
			return await send_response(interaction, "Cancelled", ephemeral=True)
		archive: discord.Category = discord.utils.get(interaction.guild.categories, name=archive_name)
		if archive is None :
			archive = await interaction.guild.create_category(name=archive_name)
		await Templater.apply(interaction, archive, template.data)
		return await send_response(interaction, f"Template '{template.name}' applied successfully!", ephemeral=True)

	@app_commands.command(name="list",
	                      description="Lists all templates you have created")
	@app_commands.checks.has_permissions(administrator=True)
	async def list_template(self, interaction: discord.Interaction) :
		templates = TemplateTransactions().get_all_templates(interaction.user.id)
		await send_response(interaction, f"Here is a list of your templates:\n{'\n* '.join([""] + templates)}", ephemeral=True)

	@app_commands.command(name="view",
	                      description="View a template you have created")
	@app_commands.autocomplete(template=auto_complete_templates)
	@app_commands.checks.has_permissions(administrator=True)
	async def view_template(self, interaction: discord.Interaction, template: str) :
		template = TemplateTransactions().get_template(interaction.user.id, template)
		if template is None:
			return await send_response(interaction, f"Template '{template}' does not exist", ephemeral=True)
		template_data: dict = template.data
		template_text = ""
		for category in template_data:
			template_text += f"**{template_data[category]['name']}**\n"
			for channel in template_data[category]["channels"] :
				template_text += f"- {channel}\n"



		embed = discord.Embed(title=f"Template '{template.name}'", description=f"Template data:\n{template_text}")
		await send_response(interaction, "", embed=embed, ephemeral=True)
		return None

	@app_commands.command(name="delete",
	                      description="Delete a template you have created")
	@app_commands.autocomplete(template=auto_complete_templates)
	@app_commands.checks.has_permissions(administrator=True)
	async def delete_template(self, interaction: discord.Interaction, template: str) :
		# Check how many templates are already registered
		if interaction.user.id in self.cache :
			self.cache.pop(interaction.user.id)

			if TemplateTransactions().delete_template(interaction.user.id, template) is False:
				return await send_response(interaction, f"Template '{template}' does not exist", ephemeral=True)
		return await send_response(interaction, f"Template '{template}' deleted successfully! You can create {MAX_TEMPLATES - TemplateTransactions().count_templates(interaction.user.id)} more templates", ephemeral=True)

	@app_commands.command(name="archivepurge", description="removes ALL archived channels, this can NOT be undone.")
	@app_commands.checks.has_permissions(administrator=True)
	async def purge(self, interaction: discord.Interaction) :
		if interaction.user.id != interaction.guild.owner.id :
			return await interaction.response.send_message("Only the owner of the server can run this command",
			                                               ephemeral=True)
		await interaction.response.defer(ephemeral=True)

		def check(m) :
			return m.content is not None and m.channel == interaction.channel

		confirm = True
		while confirm is True :
			desc = "to purge the archive, please type **'confirm'**"
			embed = discord.Embed(title=f"Purge Archive?", description=desc)
			conf = await interaction.channel.send(embed=embed)
			msg = await self.bot.wait_for('message', check=check)
			if "confirm" in msg.content.lower() :
				desc = "Confirmation received, archive will be purged."
				embed = discord.Embed(title=f"Purge Archive?", description=desc)
				confirm = False
				await conf.edit(embed=embed)
				await msg.delete()
				sleep(3)
		categories = [category for category in interaction.guild.categories if category.name.lower().startswith("archive")]
		for category in categories :
			for channel in category.channels :
				await channel.delete()
			await category.delete()


async def setup(bot) :
	await bot.add_cog(Templates(bot))
