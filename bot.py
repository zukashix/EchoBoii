import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

from discord.ext import commands
import discord
import aiohttp
import json
from pretty_help import PrettyHelp
import os

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=['eB ','Eb ','eb ','EB '], intents=discord.Intents.all(), help_command=PrettyHelp())
        self.initial_extensions = [
            'plugins.errorHandler',
            'plugins.fun',
            'plugins.games',
            'plugins.guess_music',
            'plugins.help',
            'plugins.music',
            'plugins.SUtils',
            'plugins.utilities',
            'plugins.youtube'
        ]

        if not os.path.isfile('data/build.json'):
            buildDict = {'CurrentBuild':'Unknown'}
            json.dump(buildDict, open('data/build.json', 'w'))
            prLog.warning("Build file not found, written unknown")

        prLog.debug("Bot initialize success")

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        prLog.debug("Loaded plugins")

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the impostor being sus"))
        prLog.info("Bot is ready")

bot = MyBot()
bot.run(json.load(open("data/api_keys.json", 'r'))["Discord_Bot_TOKEN"])
