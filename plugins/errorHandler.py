from discord.ext import commands
import traceback
import json
import requests
import datetime

WEBHOOK_URL = json.load(open('data/urls.json', 'r'))["Webhook_URL"]

class ExceptionHandler(commands.Cog):
    """Ignore. This cog handles runtime errors"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            tbc = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            tbctext = ''

            for i in tbc:
                tbctext += i

            url = WEBHOOK_URL
            timestamp = str(datetime.datetime.utcnow())
            await ctx.send('An internal error occurred! We are very sorry.\nPease DM the following to `Zukashi#7071`:')
            await ctx.send('`ZDPY-ECHORW2_{}`'.format(timestamp))
            msg = 'ZDPY-ECHORW2_{}\n```{}```'.format(timestamp, tbctext)
            data = {
                'content': msg
            }

            requests.post(url, data)

    # @commands.command()
    # async def errortest(self, ctx):
    #     raise Exception('valid exception')

async def setup(bot):
    await bot.add_cog(ExceptionHandler(bot))
