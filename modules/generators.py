import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from classes import Gen


class Generators(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="firstname", description="Generate up to 50 names for your character")
    @app_commands.choices(gender=[
        Choice(name="Male", value="m"),
        Choice(name="Female", value="f"),
        # Choice(name="enby", value="n"),
    ])
    async def fngen(self, interaction: discord.Interaction, gender: Choice[str], amount: int = 10):
        await interaction.response.defer(thinking=False)
        if amount > 50:
            await interaction.followup.send("You can not generate more than 50 names at once.")
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

    @app_commands.command(name="lastname", description="Generate up to 50 names for your character")
    async def lngen(self, interaction: discord.Interaction, amount: int = 10):
        await interaction.response.defer(thinking=False)
        if amount > 50:
            await interaction.followup.send("You can not generate more than 50 names at once.")
            return
        names = await Gen.lname(amount)
        n = "\n".join(names)
        embed = discord.Embed(title=f"{amount} last names generated:", description=f"{n}")
        await interaction.followup.send(embed=embed)

            # case "n":
            #     print("n name")

    @app_commands.command(name="fullname", description="Generate up to 50 first and last names for your character")
    @app_commands.choices(gender=[
        Choice(name="Male", value="m"),
        Choice(name="Female", value="f"),
    ])
    async def ngen(self, interaction: discord.Interaction, gender: Choice[str], amount: int = 10):
        await interaction.response.defer(thinking=False)
        fullnames = []
        if amount > 50:
            await interaction.followup.send("You can not generate more than 50 names at once.")
            return
        match gender.value:
            case "m":
                firstnames = await Gen.name(gender.value, amount)
                lastnames = await Gen.lname(amount)
                for f, l in zip(firstnames, lastnames):
                    fullnames.append(f + " " + l)
                n = "\n".join(fullnames)
                embed = discord.Embed(title=f"{amount} {gender.name} names generated:", description=f"{n}")
                await interaction.followup.send(embed=embed)
            case "f":
                firstnames = await Gen.name(gender.value, amount)
                lastnames = await Gen.lname(amount)
                for f, l in zip(firstnames, lastnames):
                    fullnames.append(f + " " + l)
                n = "\n".join(fullnames)
                embed = discord.Embed(title=f"{amount} {gender.name} names generated:", description=f"{n}")
                await interaction.followup.send(embed=embed)
            # case "n":
            #     print("n name")





async def setup(bot):
    await bot.add_cog(Generators(bot))
