import discord
from discord import app_commands
from discord.ext import commands
import random
from translate import Translator

from data.languages import LANGUAGES


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dice", description="rolls a dice for you!")
    async def dice(self, interaction: discord.Interaction, dicetype: int, amount: int = 1):
        await interaction.response.defer(thinking=False, ephemeral=True)
        if dicetype < 2:
            interaction.followup.send("Please choose a dice with at least 2 sides!")
            return
        if dicetype > 1000:
            interaction.followup.send("Please choose a dice with less than 1000 sides!")
            return
        if amount > 10:
            interaction.followup.send("you can roll up to 10 dice!")
            return
        x = 0
        results = []
        while x < amount:
            x += 1
            results.append(random.randint(1, dicetype))
        rm = map(str, results)
        t = ", ".join(rm)
        counted = sum(results)
        await interaction.channel.send(f"Results for {amount}d{dicetype}: {t} (total: {counted})")

    @app_commands.command(name="coinflip", description="flips a coin for you!")
    async def coin(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False, ephemeral=True)
        r = random.randint(1, 2)
        if r == 1:
            await interaction.channel.send(f"Heads!")
        else:
            await interaction.channel.send(f"Tails!")

    async def lang_autocomplete(self, interaction: discord.Interaction, current: str):

        return [app_commands.Choice(name=value, value=key) for key, value in LANGUAGES.items() if value.lower().startswith(current.lower())][:25]


    @app_commands.command(name="translate", description="translates a message to another language")
    @app_commands.autocomplete(from_lang=lang_autocomplete, target_language=lang_autocomplete)
    async def translator(self, interaction: discord.Interaction, text: str, from_lang :str = "en", target_language: str = "en"):
        translate = Translator(from_lang=from_lang.lower(),to_lang=target_language.lower())
        translation = translate.translate(text)
        await interaction.response.send_message(f"Translated from {from_lang} to {target_language} ```{translation}```", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Tools(bot))
