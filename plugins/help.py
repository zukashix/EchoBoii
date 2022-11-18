import discord
from discord.ext import commands
from time import sleep
import datetime
import time
import platform
import json

from sys import version_info as pyv
from discord import __version__ as dcv

start_time = time.time()

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='about', brief='Description about bot.')
    async def about(self, ctx):
        print(f'debug: TRIGGER: about command triggered by {ctx.author} at {ctx.author.guild}')
        about_bot = "Hello from EchoBoii!\n---------------------\nThis is a discord bot made for fun games and utility commands (shitty outdated description and yes im too lazy to update it).\n---------------------\nThe bot was created and being managed by Zukashi#7071 and BraxtonElmer#idkWhatsHisTag\nPlease DM Zukashi#7071 if there are any bugs or use the suggest command"
        await ctx.send(f"```{about_bot}```")
        print(f'debug: TRIGGER: about command complete at {ctx.author.guild}')

    @commands.command(name='botserverdata', brief='List of servers the bot is in')
    async def botserverdata(self, ctx):
        if ctx.author.id == 463657352386707456:
            await ctx.send('List of servers the bot is in:')
            for serv in self.bot.guilds:
                await ctx.send(serv)
        else:
            await ctx.send('You are not authorized to perform this action.')

    @commands.command(name='status', brief='Get bot\'s status')
    async def status(self, ctx, technef = 'None'):
        print(f"debug: TRIGGER: status command triggered by {ctx.author} at {ctx.author.guild}")
        bot_ping = int(self.bot.latency * 1000)
        bot_servers = len(self.bot.guilds)
        bot_status = "Online"
        bot_stz = "UTC"
        bot_version = str(json.load(open('data/api_keys.json', 'r'))["BotVersion"])
        bot_build = str(json.load(open('data/build.json', 'r'))["CurrentBuild"])
        bot_host = str(platform.node())
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(title = "Bot Status!", colour = self.bot.user.colour)

        embed.set_footer(text = f"Command executed by {ctx.author}")
        embed.set_thumbnail(url = self.bot.user.avatar.url)

        embed.add_field(name = "Bot's Status:", value = bot_status, inline = False)
        embed.add_field(name = "Bot's Ping:", value = bot_ping, inline = False)
        embed.add_field(name = "Standard TimeZone:", value = bot_stz, inline = False)
        embed.add_field(name = "Server Count:", value = bot_servers, inline = False)
        embed.add_field(name = "Bot's Uptime:", value = uptime, inline = False)
        embed.add_field(name = "Bot's Version:", value = bot_version, inline = False)

        await ctx.send(embed = embed)

        if technef.lower() == 'techinf':
            await ctx.send("**Techincal Information:**")
            await ctx.send("```\nPython: {}.{}.{}\n---------------\nDiscord.py: {}\n---------------\nHost Device: {}\n---------------\nBuild: {}```".format(pyv.major, pyv.minor, pyv.micro, dcv, bot_host, bot_build))

        print(f"debug: TRIGGER: status command complete at {ctx.author.guild}")

async def setup(bot):
    await bot.add_cog(Debug(bot))
