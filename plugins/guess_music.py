from lib import gtb_api as gtba
from discord.ext import commands, tasks
import asyncio

class GuessMus(commands.Cog, name='Guess The Music'):
    """Fun games to play with the bot!"""
    def __init__(self, bot):
        self.bot = bot
        self.channel = 0
        self.timeOver = False
        self.tenS = False
        self.songdata = ()
        self.larr = []

    @tasks.loop()
    async def gtmTimeout(self):
        await asyncio.sleep(60)
        self.timeOver = True
        nch = self.bot.get_channel(self.channel)
        await nch.send("Oops. The time is up!!\nThe song was: **{}** by **{}**".format(self.songdata[0], self.songdata[1]))

    @tasks.loop()
    async def gtmLyricsExposer(self):
        nch = self.bot.get_channel(self.channel)
        while self.larr != []:
            await asyncio.sleep(15)
            await nch.send('Here\'s another 4 lines of the lyrics')
            msg = '```'
            for i in self.larr[:4]:
                msg += f'\n{i}'

            msg += '\n```'
            await nch.send(msg)
            larr = self.larr[4:]
        
        await asyncio.sleep(60)

    @commands.command(name='gtm', brief='Guess the music game!', description='A guessing game in which you will have 60 seconds and you will be given a song\'s lyrics every 15 seconds. You must guess it to win!')
    async def gtm(self, ctx):

        await ctx.send("Finding a song for you!!")
        songdat = gtba.return_song()
        larr = gtba.get_lyrics(songdat[0], songdat[1])
        if larr == None:
            await ctx.send('The API could not find the song\'s lyrics. Please retry :crying_cat_face:')
        else:
            await ctx.send('Ooookay, things are now ready. You all have **60 secs** to guess the song!!')
            await ctx.send('Also, 4 Lines of lyrics will be revealed every 15 seconds!!')
            timecount = await ctx.send('Starting in 3... ')
            await asyncio.sleep(1)
            await timecount.edit(content="Starting in 3... 2... ")
            await asyncio.sleep(1)
            await timecount.edit(content="Starting in 3... 2... 1... ")
            await asyncio.sleep(1)
            await timecount.edit(content="Starting in 3... 2... 1... GO GO GO!!!")

            await ctx.send('Here\'s first 4 lines of the lyrics!!')
            msg = '```'
            for i in larr[:4]:
                msg += f'\n{i}'

            msg += '\n```'
            await ctx.send(msg)
            larr = larr[4:]

            self.channel = ctx.channel.id
            self.songdata = songdat

            def check(m):
                return m.channel == ctx.channel

            self.larr = larr

            self.gtmTimeout.start()
            self.gtmLyricsExposer.start()

            while self.timeOver == False:
                msg = await self.bot.wait_for('message', check=check)

                if self.timeOver:
                    self.gtmTimeout.cancel()
                    self.gtmLyricsExposer.cancel()
                    break

                if msg.content.lower() == songdat[0].lower():
                    await ctx.send("{}, I think you guessed the song!! YOU WIN!!\nThe song was: **{}** by **{}**".format(msg.author.name, songdat[0], songdat[1]))
                    self.gtmTimeout.cancel()
                    self.gtmLyricsExposer.cancel()
                    break

                if msg.content.lower() == songdat[1].lower():
                    await ctx.send("{}, I think you guessed the author! Now go for the song!!".format(msg.author.name))
                    continue

async def setup(bot):
    await bot.add_cog(GuessMus(bot))
