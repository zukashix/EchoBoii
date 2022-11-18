import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

import discord
import random
from discord.ext import commands
from time import sleep
import aiohttp
import json

MEME_FETCH_URL = json.load(open('data/urls.json', 'r'))["Memes_URL"]
prLog.debug("Meme URL fetched")

spamLoop = True
spamRunning = False

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spamFlag = False

    @commands.command(name='rickroll', brief='Rickroll someone!')
    async def rickroll(self, ctx, *, user: discord.Member = None):
        prLog.info(f"rickroll command started by {ctx.author} at {ctx.author.guild}")

        if user == None:
            user = ctx.author

        rickroll_text = '***Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you***'
        if user is ctx.author:
            await ctx.send("You wanna RickRoll yourself? awwww, too lonely? I'll do it for you :blush:")
            await ctx.send(rickroll_text)
            await ctx.send("There, you feel better now? :upside_down:")
        else:
            welcome_text = f'Hey {user.display_name}, This is for you :upside_down:'
            end_text = f'There, You just got RickRolled by {ctx.author.display_name} :joy_cat:'
            await ctx.send(welcome_text + "\n" + rickroll_text + "\n" + end_text)
            
        prLog.info(f"rickroll command finished by {ctx.author} at {ctx.author.guild}")

    @commands.command(name='spam', brief='Spam without hassle!!', description='This command spams text/images with one command. WARNING: To avoid spamming on main channels, the spam channel must contain the word \'spam\' in it, or the command will fail.')
    async def spam(self, ctx, numberOftimes, content):
        prLog.info(f"spam command started by {ctx.author} at {ctx.author.guild}")

        try:
            int(numberOftimes)
        except:
            await ctx.send('Pass a number at the place of the \'numberOftimes\' variable. See help for more information.')

        if '@everyone' in str(content):
            await ctx.send("`@everyone` spam ping not allowed")
            return

        if '@' in str(content):
            await ctx.send('Sorry, You can\'t put \'@\' in your message. This is to avoid spam pings')
            return

        if 'spam' not in (ctx.channel.name).lower():
            await ctx.send('The channel\'s name doesn\'t contain the word \'spam\' in it.')
            return

        if int(numberOftimes) > 100:
            await ctx.send('Only 100 messages/images spam at a time!')
            return

        for i in range(int(numberOftimes)):
            if not self.spamFlag:
                await ctx.send(content)
            else:
                await ctx.send('Spam has been stopped!!')
                self.spamFlag = False
                break

        prLog.info(f"spam command finished by {ctx.author} at {ctx.author.guild}")

    @commands.command(name='spamStop', brief='Stop a running spam.', description='This command stops a running spam. WARNING: This command is currently unstable and will stop any spam in any server. So consider not using it if not important. (PS: We\'re still trying to find a better way to spam)')
    async def spamStop(self, ctx):
        prLog.info(f"spamStop command started by {ctx.author} at {ctx.author.guild}")
        self.spamFlag = True
        prLog.info(f"spamStop command finished by {ctx.author} at {ctx.author.guild}")

    @commands.command(name='meme', brief='Show a meme from reddit.')
    async def meme(self, ctx):
        prLog.info(f"meme command started by {ctx.author} at {ctx.author.guild}")

        embed = discord.Embed(title = "Meme!", colour = ctx.author.colour)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(MEME_FETCH_URL) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                embed.set_footer(text = f"Command executed by {ctx.author}")
                await ctx.send(embed = embed)

        prLog.info(f"meme command finished by {ctx.author} at {ctx.author.guild}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
    prLog.debug("Plugin fun is loaded")
