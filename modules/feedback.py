import discord
from discord import app_commands
from discord.ext import commands


class FeedBack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Sends feedback to the developer")
    async def feedback(self, interaction: discord.Interaction, *, feedback: str):
        await interaction.response.defer(thinking=False, ephemeral=True)
        fc = self.bot.get_channel(1062803821702684802)
        await fc.send(f"{interaction.user}({interaction.user.id}): {feedback}")
        await interaction.followup.send("feedback submitted! thank you!")

    @app_commands.command(name="help", description="review the help documents")
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_message("You can review the help documents here:", ephemeral=True)


async def setup(bot):
    await bot.add_cog(FeedBack(bot))
