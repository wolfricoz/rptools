import json
import os
from datetime import datetime
from time import sleep
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from classes import Templater


# noinspection PyTypeChecker
class Server(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    async def auto_complete_templates(self, interaction, current: str):
        templates = [file[:-5] for file in os.listdir('templates')]
        return [Choice(name=template, value=template) for template in templates if template.lower().startswith(current.lower())]

    @app_commands.command(name="template", description="Applies a template to your server and archives old channels. 'help' for templates")
    @app_commands.autocomplete(template=auto_complete_templates)
    async def template(self, interaction: discord.Interaction, template: str):
        await interaction.response.defer(thinking=False)
        if len(interaction.guild.members) >= 10:
            await interaction.followup.send("[Safeguard] Guild has more than 10 users, command will not run")
            return
        archive_name = f"archive-{datetime.now().strftime('%d-%m-%Y')}"
        if interaction.user == interaction.guild.owner:
            def check(m):
                return m.content is not None and m.channel == interaction.channel
            confirm = True
            try:
                with open(f'templates/{template}.json', 'r') as f:
                    while confirm is True:
                        desc = "to apply this template, please type **'confirm'**"
                        embed = discord.Embed(title=f"Apply template?", description=desc)
                        conf = await interaction.channel.send(embed=embed)
                        msg = await self.bot.wait_for('message', check=check)
                        if "confirm" in msg.content.lower():
                            desc = "Confirmation given, applying template now."
                            embed = discord.Embed(title=f"Apply template?", description=desc)
                            confirm = False
                            await conf.edit(embed=embed)
                            await msg.delete()
                            sleep(3)
                    data = json.load(f)
                    archive: discord.Category = discord.utils.get(interaction.guild.categories, name=archive_name)
                    if archive is  None:
                        archive = await interaction.guild.create_category(name=archive_name)
                    await Templater.apply(interaction, archive, data)
                    desc = "to clear the archive please use **/server archivepurge**"
                    embed = discord.Embed(title=f"Template successfully applied!", description=desc)
                    await conf.edit(embed=embed)

            except Exception as e:
                print(e)
                templates = []
                for file in os.listdir('templates'):
                    templates.append(file[:-5])
                temps = "\n- ".join(templates)
                await interaction.followup.send(f"- {temps}")
        else:
            await interaction.followup.send("[Safeguard] No permission")

    @app_commands.command(name="archivepurge", description="removes ALL archived channels, this can NOT be undone.")
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.guild.owner.id :
            return await interaction.response.send_message("Only the owner of the server can run this command", ephemeral=True)
        await interaction.response.defer(ephemeral=True)

        def check(m) :
            return m.content is not None and m.channel == interaction.channel

        confirm = True
        while confirm is True:
            desc = "to purge the archive, please type **'confirm'**"
            embed = discord.Embed(title=f"Purge Archive?", description=desc)
            conf = await interaction.channel.send(embed=embed)
            msg = await self.bot.wait_for('message', check=check)
            if "confirm" in msg.content.lower():
                desc = "Confirmation received, archive will be purged."
                embed = discord.Embed(title=f"Purge Archive?", description=desc)
                confirm = False
                await conf.edit(embed=embed)
                await msg.delete()
                sleep(3)
        categories = [category for category in interaction.guild.categories if category.name.lower().startswith("archive")]
        for category in categories:
            for channel in category.channels:
                await channel.delete()
            await category.delete()



async def setup(bot):
    await bot.add_cog(Server(bot))
