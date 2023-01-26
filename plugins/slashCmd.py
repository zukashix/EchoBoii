import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

import discord
from discord import app_commands
from discord.ext import commands

class slashCMD(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.command(name='applSync')
  async def applSync(self, ctx):
    if ctx.author.id == 463657352386707456:
      await self.bot.tree.sync()
      await ctx.send("Commands synced!")
    else:
      await ctx.send("Who are you anyway?")
    
  @app_commands.command(name="givemebadge")
  async def gmbadge(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Did it work? YES IT DID LETS EFFIN GO", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(slashCMD(bot))
  prLog.debug("Plugin slashCmd is loaded")