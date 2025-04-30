import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from classes.Generators import Gen


class Generators(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="name", description="Generate up to 20 names for your character")
    @app_commands.choices(gender=[
        Choice(name="Male", value="m"),
        Choice(name="Female", value="f"),
        # Choice(name="enby", value="n"),
    ])
    async def ngen(self, interaction: discord.Interaction, gender: Choice[str], amount: int = 10):
        await interaction.response.defer(thinking=False)
        if amount > 20:
            await interaction.followup.send("You can not generate more than 20 names at once.")
            return
        match gender.value:
            case "m":

                names = await Gen.name(gender.value, amount)
                n = "\n".join(names)
                embed = discord.Embed(title=f"{amount} {gender.name} names generated:", description=f"{n}")
                await interaction.followup.send(embed=embed)
            case "f":
                names = await Gen.name(gender.value, amount)
                n = "\n".join(names)
                embed = discord.Embed(title=f"{amount} {gender.name} names generated:", description=f"{n}")
                await interaction.followup.send(embed=embed)
            # case "n":
            #     print("n name")


async def setup(bot):
    await bot.add_cog(Generators(bot))
