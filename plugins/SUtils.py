from discord import Embed
from discord.ext import commands

import requests
import json
import re
import lxml.html as htm
from urllib.parse import quote as urlfix
from googletrans import Translator
from langcodes import *
import datetime, pytz
from pytz.exceptions import UnknownTimeZoneError as UTZE

def convert24(str1):
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]
  
    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]
          
    else:
        return str(int(str1[:2]) + 12) + str1[2:8]

translator = Translator()

def cleanBraces(rtext):
  return re.sub(r"\[[^[]]*\]", "", rtext)

class SUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='weather', brief='Show current weather of a location')
    async def weather(self, ctx,  *, city):
        print(f"debug: TRIGGER: weather command triggered by {ctx.author} at {ctx.author.guild}")
        requestURL = (str(json.load(open('data/urls.json', 'r'))["Weather_API_URL"]).replace("!!CITY_NAME_GOES_HERE!!", city)).replace('!!API_KEY_GOES_HERE!!', json.load(open('data/api_keys.json', 'r'))["Weather_API_KEY"])
        data = requests.get(requestURL).json()
        cleared_data = {
            'City': data['name'],
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']}Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h"
        }
        embed = Embed(title=f":white_sun_small_cloud: Weather in {cleared_data['City']}", color=0x3498db)
        for key, value in cleared_data.items():
            embed.add_field(name=key, value=value)
        await ctx.send(embed=embed)
        print(f"debug: TRIGGER: weather command complete at {ctx.author.guild}")
        
    @commands.command(name="Wikipedia", aliases=['wiki', 'wikipedia'], brief="Get summary of a wikipedia article", description="This commands gets summary of a topic from a wikipedia article. Usage: eb wiki Bruno Mars")
    async def wikipedia(self, ctx, *, query):
        requestUrl = str(json.load(open('data/urls.json', 'r'))["Wikipedia_URL"]).replace('!!QUERY_GOES_HERE!!', urlfix(query))
        data = requests.get(requestUrl)
        if data.status_code != 200:
            await ctx.send('Sorry, could not find any data. Try removing any extra spaces or an \'s\'.\nExample: Type \'fruit\' instead of \'fruits\'\nDetails: `STATUS_CODE != 200')
        else:
            await ctx.send(cleanBraces(htm.fromstring(data.text.split('<p>')[1].split('</p>')[0]).text_content()))

    @commands.command(name="translate", aliases=['gtrans'], brief='Translate text to a wide variety of languages.', description='This command translates text to another language. Usage: eb translate en jus de chocolat (Output -> Chocolate Juice)')
    async def gtrans(self, ctx, langcode, *, text):
        tobj = translator.translate(text, dest=langcode)
        srcl = Language.make(language=tobj.src).display_name()
        await ctx.send('**__Original Text:__** {}\n**__Translated Text:__** {}\n**__Pronounciation:__** {}\n**__Source Language:__** {}'.format(text, tobj.text, tobj.pronunciation, srcl))

    @commands.command(name='suggest', brief='Suggest something for the bot', description='This command sends us (the developers) a message. So you can give us a suggestion. Example: a suggestion to bring back a command from the legacy version of the bot.')
    async def suggest(self, ctx, *, msg):
        url = json.load(open('data/urls.json', 'r'))["Webhook_URL"]
        timestamp = str(datetime.datetime.utcnow())
        msg = 'DPY-001_{} (SUGESSTION MESSAGE)\n```{}```'.format(timestamp, msg)
        data = {
            'content': msg
        }

        requests.post(url, data)
        
        await ctx.send('Message Sent :white_check_mark:')

    # UNDER DEVELOPENT, DOESNT WORK YET
    @commands.command(name='timein', brief='Get your time in some other timezone!!', description='This command will convert a given time of your timezone to another specified timezone. Supports both 12-hour time and 24-hour time input. Outputs 24-hour time. Only accepts timezone regions like \'Asia/Kolkata\' as parameters. Formats like \'EST\' or \'IST\' are not allowed!')
    async def timein(self, ctx, your_tz, convert_time, convertTo_tz):
        local_time = str(convert_time)
        local_tz = str(your_tz)
        convert_tz = str(convertTo_tz)

        await ctx.send('Converting . . . /')
        local_time = local_time.split(':')

        try:
            local_pytz = pytz.timezone(local_tz)
        except UTZE:
            await ctx.send('Timezones should be in the following format:\n`Asia/Kolkata`\nPlease avoid using format like:\n`IST` or `CEST`')

        utcnow = datetime.datetime.utcnow()
        timestr = f'{local_time[0]}:{local_time[1]}'
        datetime_tobj = datetime.datetime.strptime(timestr, '%H:%M')

        try:
            converted_dtobj = datetime_tobj.astimezone(pytz.timezone(convert_tz))
        except UTZE:
            await ctx.send('Timezones should be in the following format:\n`Asia/Kolkata`\nPlease avoid using format like:\n`IST` or `CEST`')

        await ctx.send('**Converted Time:** {}:{}'.format(converted_dtobj.hour, converted_dtobj.minute))

async def setup(bot):
    await bot.add_cog(SUtils(bot))
