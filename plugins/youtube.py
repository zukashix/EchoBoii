import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

import discord  # discord api
from discord.ext import commands  # commands extension
from apiclient.discovery import build  # youtube api
import json
from datetime import datetime
import sys
import aiohttp
import re

# Some systems will crash without this because Google's Python is built differently
sys.modules['win32file'] = None
youtube_key = json.load(open('data/api_keys.json', 'r'))["Youtube_API_KEY"]
prLog.debug("Loaded youtube key")

class YouTube(commands.Cog):
    """Youtube Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    @commands.group()
    async def yt(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(":x: **Missing/Invalid Subcommand**")
            prLog.info(f'yt recieved a missing/invalid subcommand by {ctx.author} at {ctx.author.guild}')

    @yt.command(aliases=["s"], name='search', brief='Search a video on youtube')
    async def search(self, ctx):
        prLog.info(f'yt search command started by {ctx.author} at {ctx.author.guild}')

        try:
            if len(ctx.message.content.split(' ', 3)) == 3:
                await ctx.send("Arguments needed!\n\nExample: `eB yt search Darude Sandstorm`")
            else:
                youtube = build("youtube", "v3", developerKey=youtube_key)
                search_response = youtube.search().list(q=ctx.message.content.split(
                    ' ', 3)[3], part="id,snippet", maxResults=1, type="video").execute()
                if len(search_response.get('items')) == 0:
                    await ctx.send("No videos found.")
                else:
                    vidid = search_response.get('items')[0]['id']['videoId']
                    vidurl = "https://www.youtube.com/watch?v=" + vidid
                    yt_url = "https://www.youtube.com/oembed?url={0}&format=json".format(
                        vidurl)
                    metadata = await self.get_json(yt_url)
                    data = discord.Embed(
                        title="**__Search Result__**", colour=discord.Colour(value=11735575))
                    data.add_field(name="Video Title", value=metadata[
                                   'title'], inline=False)
                    data.add_field(name="Video Uploader", value=metadata[
                                   'author_name'], inline=False)
                    data.add_field(name="Video Link",
                                   value=vidurl, inline=False)
                    data.set_image(
                        url="https://i.ytimg.com/vi/{}/hqdefault.jpg".format(vidid))
                    data.set_footer(
                        text=f"Command executed by {ctx.author}")
                    try:
                        await ctx.send(embed=data)
                    except discord.HTTPException:
                        await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        except Exception as e:
            data = discord.Embed(title="__***Error in video search!***__",
                                 description="No data for video ID!", colour=discord.Colour(value=11735575))
            data.add_field(name="Whoops!", value="Looks like the API returned a video, but there is no associated data with it!\nThis could be due to the video being unavailable anymore, or it is country blocked!", inline=False)
            data.add_field(name="What can I do now?",
                           value="Not much really. *__Please don't re-search the video__*, as this adds unnecessary strain on the bot, and you'll get the same result.", inline=False)
            data.set_footer(text=f"Command executed by {ctx.author}")
            try:
                await ctx.send(embed=data)
            except discord.HTTPException:
                await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        
        prLog.info(f'yt search command finished by {ctx.author} at {ctx.author.guild}')

    @yt.command(aliases=["c"], name='channel', brief='Search for a youtube channel')
    async def channel(self, ctx):
        prLog.info(f'yt channel command started by {ctx.author} at {ctx.author.guild}')

        try:
            if len(ctx.message.content.split(' ', 3)) == 3:
                await ctx.send("Arguments needed!\n\nExample: `eB yt channel TrapNation`")
            else:
                youtube = build("youtube", "v3", developerKey=youtube_key)
                search_response = youtube.search().list(q=ctx.message.content.split(
                    ' ', 3)[3], part="id,snippet", maxResults=1, type="channel").execute()
                if len(search_response.get('items')) == 0:
                    await ctx.send("No channels found.")
                else:
                    chanid = search_response.get('items')[0]['id']['channelId']
                    data = youtube.channels().list(part='statistics,snippet', id=chanid).execute()
                    subs = str(data['items'][0]['statistics']
                               ['subscriberCount'])
                    subsf = await self.thous(subs)
                    name = str(data['items'][0]['snippet']['title'])
                    img = str(data['items'][0]['snippet'][
                              'thumbnails']['medium']['url'])
                    chanurl = "https://www.youtube.com/channel/" + chanid
                    data = discord.Embed(
                        title="**__Search Result__**", colour=discord.Colour(value=11735575))
                    data.add_field(name="Channel Name",
                                   value=name, inline=False)
                    data.add_field(name="Subscribers",
                                   value=subsf, inline=False)
                    data.add_field(name="Channel Link",
                                   value=chanurl, inline=False)
                    data.set_image(url=img)
                    data.set_footer(
                        text=f"Command executed by {ctx.author}")
                    try:
                        await ctx.send(embed=data)
                    except discord.HTTPException:
                        await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        except Exception as e:
            data = discord.Embed(title="__***Error in channel search!***__",
                                 description="No data for channel ID!", colour=discord.Colour(value=11735575))
            data.add_field(name="Whoops!", value="Looks like the API returned a channel, but there is no associated data with it!\nThis could be due to the video being unavailable anymore, or it is country blocked!", inline=False)
            data.add_field(name="What can I do now?",
                           value="Not much really. *__Please don't re-search the channel__*, as this adds unnecessary strain on the bot, and you'll get the same result.", inline=False)
            data.set_footer(text=f"Command executed by {ctx.author}")
            try:
                await ctx.send(embed=data)
            except discord.HTTPException:
                await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        prLog.info(f'yt channel command finished by {ctx.author} at {ctx.author.guild}')

    @yt.command(aliases=['l'], name='lookup', brief='Reverse lookup a youtube video')
    async def lookup(self, ctx):
        prLog.info(f'yt lookup command started by {ctx.author} at {ctx.author.guild}')

        try:
            if len(ctx.message.content.split(' ', 3)) == 3:
                await ctx.send("Arguments needed!\n\nExample: `eB yt lookup https://www.youtube.com/watch?v=dQw4w9WgXcQ`")
            else:
                url = re.compile(
                    r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?')
                shorturl = re.compile(
                    r'http(?:s?):\/\/?youtu(?:\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?')
                q = ctx.message.content.split(' ', 3)[3]
                match = re.search(url, q)
                if match:
                    match2 = re.search(shorturl, q)
                    if match2:
                        a = match2.group(1)
                        q = 'https://www.youtube.com/watch?v={}'.format(a)
                    yt_url = "https://www.youtube.com/oembed?url={0}&format=json".format(
                        q)
                    metadata = await self.get_json(yt_url)
                    youtube = build("youtube", "v3", developerKey=youtube_key)
                    search_response = youtube.search().list(q=ctx.message.content.split(
                        ' ', 3)[3], part="id,snippet", maxResults=1, type="video").execute()
                    if len(search_response.get('items')) == 0:
                        await ctx.send("No videos found.")
                    else:
                        vidid = search_response.get(
                            'items')[0]['id']['videoId']
                        data = discord.Embed(
                            title="**__Reverse Lookup__**", colour=discord.Colour(value=11735575))
                        data.add_field(name="Video Title", value=metadata[
                                       'title'], inline=False)
                        data.add_field(name="Video Uploader", value=metadata[
                                       'author_name'], inline=False)
                        data.add_field(name="Video Link",
                                       value=q, inline=False)
                        data.set_image(
                            url="https://i.ytimg.com/vi/{}/hqdefault.jpg".format(vidid))
                        data.set_footer(
                            text=f"Command executed by {ctx.author}")
                    try:
                        await ctx.send(embed=data)
                    except discord.HTTPException:
                        await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
                else:
                    await ctx.send("Whoops! Looks like you didn't specify a URL for me to lookup!")
        except Exception as e:
            data = discord.Embed(title="__***Error in reverse lookup!***__",
                                 description="No data for video ID!", colour=discord.Colour(value=11735575))
            data.add_field(name="Whoops!", value="Looks like the API returned info for the video, but there is no associated data with it!\nThis could be due to the video being unavailable anymore, or it is country blocked!", inline=False)
            data.add_field(name="What can I do now?",
                           value="Not much really. *__Please don't re-search the video__*, as this adds unnecessary strain on the bot, and you'll get the same result.", inline=False)
            data.set_footer(text=f"Command executed by {ctx.author}")
            try:
                await ctx.send(embed=data)
            except discord.HTTPException:
                await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        
        prLog.info(f'yt lookup command finished by {ctx.author} at {ctx.author.guild}')

    @yt.command(aliases=['n'], name='new', brief='Find newest video of a channel')
    async def new(self, ctx):
        prLog.info(f'yt new command started by {ctx.author} at {ctx.author.guild}')

        try:
            if len(ctx.message.content.split(' ', 3)) == 3:
                await ctx.send("Arguments needed!\n\nExample: `eB yt new Kurzgesagt`")
            else:
                youtube = build("youtube", "v3", developerKey=youtube_key)
                search_response = youtube.search().list(q=ctx.message.content.split(
                    ' ', 3)[3], part="id,snippet", maxResults=1, type="channel").execute()
                if len(search_response.get('items')) == 0:
                    await ctx.send("No channels found.")
                else:
                    chanid = search_response.get('items')[0]['id']['channelId']
                channelDetails = youtube.channels().list(
                    id=chanid, part="contentDetails", maxResults=1).execute()
                playlistid = channelDetails['items'][0][
                    'contentDetails']['relatedPlaylists']['uploads']
                videos = youtube.playlistItems().list(
                    playlistId=playlistid, part="snippet", maxResults=1).execute()
                if len(videos.get('items')) == 0:
                    await ctx.send("No channels found.")
                else:
                    vidid = videos['items'][0]['snippet'][
                        'resourceId']['videoId']
                    title = videos['items'][0]['snippet']['title']
                    dateraw = datetime.strptime(videos['items'][0]['snippet'][
                                                'publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                    uploader = videos['items'][0]['snippet']['channelTitle']
                    # '%H:%M (GMT), %A %d %b %Y'
                    uploaddate = datetime.strftime(
                        dateraw, '%H:%M %A %d %b %Y')
                    data = discord.Embed(
                        title="**__Latest Video from {}__**".format(uploader), colour=discord.Colour(value=11735575))
                    data.add_field(name="Video Title",
                                   value=title, inline=False)
                    data.add_field(name="Upload Date",
                                   value=uploaddate, inline=False)
                    data.add_field(
                        name="Video Link", value="https://youtube.com/watch?v={}".format(vidid), inline=False)
                    data.set_image(
                        url="https://i.ytimg.com/vi/{}/mqdefault.jpg".format(vidid))
                    data.set_footer(
                        text=f"Command executed by {ctx.author}")
                try:
                    await ctx.send(embed=data)
                except discord.HTTPException:
                    await ctx.send("Looks like the bot doesn't have embed links perms... It kinda needs these, so I'd suggest adding them!")
        except Exception as e:
            print(e)

        prLog.info(f'yt new command finished by {ctx.author} at {ctx.author.guild}')

    async def get_json(self, yt_url):
        async with self.session.get(yt_url) as r:
            result = await r.json()
        return result

    async def thous(self, subs):
        return re.sub(r'(\d{3})(?=\d)', r'\1 ', str(subs)[::-1])[::-1]


async def setup(bot):
    await bot.add_cog(YouTube(bot))
    prLog.debug("Plugin youtube is loaded")
