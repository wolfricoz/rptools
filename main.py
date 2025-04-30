#!/usr/bin/env python
import logging
import os
import traceback

# imports discord
import discord
from discord import Interaction
from discord import app_commands
from discord.app_commands import AppCommandError
from discord.ext import commands
# imports dotenv, and loads items
from dotenv import load_dotenv

from database.database import create_tables

load_dotenv(".env")

create_tables()

prefix = os.getenv('PREFIX')
TOKEN = os.getenv('TOKEN')
# declares bots intents, and allows commands to be ran
intent = discord.Intents.default()
intent.message_content = True
intent.members = True
bot = commands.Bot(command_prefix=prefix, case_insensitive=False, intents=intent)

# imports database and starts it
# error logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger2 = logging.getLogger('sqlalchemy')
logger2.setLevel(logging.WARN)
handler2 = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler2.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger2.addHandler(handler2)


@bot.command()
async def sync(ctx):
    s = await ctx.bot.tree.sync()
    await ctx.send(f"bot has synced {len(s)} servers")


# noinspection PyMethodParameters
class Main:
    @bot.event
    async def on_ready():
        # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
        guild_count = 0
        guilds = []
        # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.

        for guild in bot.guilds:
            # PRINT THE SERVER'S ID AND NAME AND CHECKS IF GUILD CONFIG EXISTS, IF NOT IT CREATES.
            guilds.append(f"- {guild.id} (name: {guild.name})")

            # INCREMENTS THE GUILD COUNTER.
            guild_count += 1
        # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
        formguilds = "\n".join(guilds)
        devroom = bot.get_channel(1061362347739971694)
        # await devroom.send(f"{formguilds} \n RP server setup 1.0.0 is in {guild_count} guilds.")
        # SYNCS UP SLASH COMMANDS
        await bot.tree.sync()
        return guilds

    # @bot.event
    # async def on_guild_join(guild):
    #     #SYNCS COMMANDS
    #     await bot.tree.sync()
    #     # sends owner instructions
    #     await guild.owner.send("Thank you for inviting Age Verifier, please read https://docs.google.com/document/d/1jlDPYCjYO0vpIcDpKAuWBX-iNDyxOTSdLhn_SsVGeks/edit?usp=sharing to set up the bot")
    #     log = bot.get_channel(1022319186950758472)
    #     await log.send(f"Joined {guild}({guild.id})")

    @bot.event
    async def setup_hook():
        """Connects the cogs to the bot"""
        for filename in os.listdir("modules"):
            if filename.endswith('.py'):
                await bot.load_extension(f"modules.{filename[:-3]}")
                print({filename[:-3]})
            else:
                print(f'Unable to load {filename[:-3]}')

    tree = bot.tree

    @tree.error
    async def on_app_command_error(
            interaction: Interaction,
            error: AppCommandError
    ):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(f"No permissions", ephemeral=True)
        else:
            await interaction.followup.send(f"Command failed: {error}")
            logging.error(traceback.format_exc())
            channel = bot.get_channel(1062803745299243040)
            await channel.send(traceback.format_exc())
        # raise error


bot.run(TOKEN)
