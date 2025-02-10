import logging
import os
import time
import traceback
from datetime import datetime, timedelta
from sys import platform

import discord.utils
from discord import Interaction
from discord.app_commands import AppCommandError, command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('main.env')
channels72 = os.getenv('channels72')
spec = os.getenv('spec')
channels24 = os.getenv('channels24')
single = os.getenv('single')
test = os.getenv('test')
count = 0
os.environ['TZ'] = 'America/New_York'
if platform == "linux" or platform == "linux2":
    time.tzset()
logfile = f"logs/log-{time.strftime('%m-%d-%Y')}.txt"
removeafter = datetime.now() + timedelta(days=-7)


def extract_datetime_from_logfile(filename):
    # Split the filename by '-'
    parts = filename.split('-')
    if len(parts) >= 3:
        # Extract the date part
        date_part = parts[1] + '-' + parts[2] + '-' + parts[3].split('.')[0]
        return datetime.strptime(date_part, '%m-%d-%Y')
    return None


if os.path.exists('logs') is False:
    print("Making logd directory")
    os.mkdir('logs')

if os.path.exists(logfile) is False:
    with open(logfile, 'w') as f:
        f.write("logging started")

for file in os.listdir('logs'):
    date = extract_datetime_from_logfile(file)
    if date is not None and date < removeafter:
        logging.info(f"Removing old log file: {file}")
        os.remove(f'logs/{file}')

with open(logfile, 'a') as f:
    f.write(f"\n\n----------------------------------------------------"
            f"\nbot started at: {time.strftime('%c %Z')}\n"
            f"----------------------------------------------------\n\n")

handlers = [logging.FileHandler(filename=logfile, encoding='utf-8', mode='a'), logging.StreamHandler()]
logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s:%(name)s: %(message)s')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger2 = logging.getLogger('sqlalchemy')
logger2.setLevel(logging.WARN)


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_command_error")
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please fill in the required arguments")
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("User not found")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Command failed: See log.")
            await ctx.send(error)
            logging.warning(error)
            raise error
        else:
            await ctx.send(error)
            logging.warning(f"\n{ctx.guild.name} {ctx.guild.id}: {error}")
            raise error

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    async def on_app_command_error(
            self,
            interaction: Interaction,
            error: AppCommandError
    ):
        await interaction.followup.send(f"Command failed: {error} \nreport this to Rico")
        logger.error(traceback.format_exc())
        channel = self.bot.get_channel(1033787967929589831)
        with open('error.txt', 'w', encoding='utf-8') as f:
            f.write(traceback.format_exc())
        await channel.send(f"{interaction.guild.name} {interaction.guild.id}: {interaction.user}: ", file=discord.File(f.name, "error.txt"))
        logging.warning(f"\n{interaction.guild.name} {interaction.guild.id}: {error}")
        raise error

    @commands.Cog.listener(name='on_command')
    async def print(self, ctx):
        server = ctx.guild
        user = ctx.author
        command = ctx.command
        logging.debug(f'\n{server.name}({server.id}): {user}({user.id}) issued command: {command}')

    @commands.Cog.listener(name='on_app_command_completion')
    async def print(self, ctx: Interaction, command: command):
        server = ctx.guild
        user = ctx.user
        logging.debug(f'\n{server.name}({server.id}): {user}({user.id}) issued appcommand: {command.name}')


async def setup(bot):
    await bot.add_cog(Logging(bot))
