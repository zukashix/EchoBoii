from discord.ext import commands
import discord
import aiohttp
import json
from pretty_help import PrettyHelp

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

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the impostor being sus"))
        print('debug: EchoiBoii-RW2 Ready!')

bot = MyBot()
bot.run(json.load(open("data/api_keys.json", 'r'))["Discord_Bot_TOKEN"])
