import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

import discord
import random
from discord.ext import commands
from asyncio import sleep
from discord.ext.commands import has_permissions, CheckFailure
import datetime
import time

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='echo', brief='Make the bot say something')
    async def echo(self, ctx, *, msg = None):
        prLog.info(f'echo command started by {ctx.author} at {ctx.author.guild}')

        if msg is None:
            await ctx.send("Please define a message to echo")
        elif '@everyone' in str(msg):
            await ctx.send("@/everyone pinging not allowed")
        else:
            msg = str(msg)
            await ctx.channel.purge(limit = 1)
            await ctx.send(msg)      

        prLog.info(f'echo command finished by {ctx.author} at {ctx.author.guild}')
        
    '''@commands.command()
    async def math(self, ctx, *, equation):
        print(f'debug: TRIGGER: math command triggered by {ctx.author} at {ctx.author.guild}')
        try:
            embed = discord.Embed(colour = ctx.author.colour)

            embed.set_author(name = f"{ctx.author.display_name}'s math question")
            embed.set_footer(text = f"Command executed by {ctx.author}")

            answer = eval(equation)

            embed.add_field(name = f"Question: {str(equation)}", value = f"**Answer: {str(answer)}**")
            await ctx.send(embed = embed)

        except(NameError, SyntaxError):
            await ctx.send("That's Not A Valid Equation My Friend")
        print(f'debug: TRIGGER: math command complete at {ctx.author.guild}')'''

    @commands.command(name='typetest', brief='Test your typing speed')
    async def typetest(self, ctx):
        prLog.info(f'typetest command started by {ctx.author} at {ctx.author.guild}')

        typelist = [
            "Success comes from the inside out. In order to change what is on the outside, you must first change what is on the inside.",
            "Once you embrace your value, talents and strengths, it neutralizes when others think less of you.",
            "In every change, in every falling leaf there is some pain, some beauty. And that's the way new leaves grow.",
            "Love people who hate you. Pray for people who have wronged you. It won’t just change their life…it’ll change yours.",
            "Everything is within your power, and your power is within you.",
            "Never underestimate the power you have to take your life in a new direction.",
            "Small shifts in your thinking, and small changes in your energy, can lead to massive alterations of your end result.",
            "When God is ready for you to move, He will make your situation uncomfortable.",
            "They can rip you bring you down, down to their size, but they will never get to the heart you hold inside.",
            "To shift your life in a desired direction, you must powerfully shift your subconscious.",
            "Only by speaking out can we create lasting change. And that change begins with coming out.",
            "If you want to turn your life you're going to have to start making things happen and stop allowing things to happen to you.",
            "Life begins when we get tired of our own bullshit. We must all get bloody tired of our own bullshit, in order for our lives to begin.",
            "Shift gears every once in awhile. You don't have to stay stuck in first or neutral, both get you no where fast.",
            "When today is no different than yesterday and you haven’t taken any action to improve your tomorrow, then all your days continue to be yesterdays.",
            "When you get to a point in a situation when you say I'm too old for this or I'm too young for this, it is definitely time to make a change.",
            "To change your life, change something you do daily.",
            "Nothing will change outside until you change everything inside.",
            "Before anyone can improve their life, they must get the idea that change is possible, that life can be different and better, and that it is worth the effort it takes to make it happen.",
            "You are allowed a do-over if you don't like the way things are going.",
            "When life gives you lemon, make cannabis infused lemon bars."
        ]

        chosen_typesent = random.choice(typelist)
        await ctx.send("**INSTRUCTIONS:**\n\n**All the sentences are case-sensitive.**\n**There is no time limit**\n**Each and every exclamation/comma/period matters**")
        await ctx.send(f'You have to start typing\n"`{chosen_typesent}`"\nin 3s')
        sleep(1)
        await ctx.send("2s")
        sleep(1)
        await ctx.send("1s")
        sleep(1)
        await ctx.send("GO!")
        type_start_time = time.time()
        msg = await self.bot.wait_for('message', check = None)
        msgf = msg.content
        while msg.author != ctx.author:
            msg = await self.bot.wait_for('message', check = None)
        if msg.author == ctx.author:
            msgf = msg.content
            type_end_time = time.time()
            difference = int(round(type_end_time - type_start_time))
            time_taken = str(datetime.timedelta(seconds=difference))
            if msgf == chosen_typesent:
                await ctx.send(f'You Typed:\n"**{msgf}**"\nTime Taken: {time_taken}')
            else:
                await ctx.send(f'**You couldnt type the exact thing**\n**What you had to type:** {chosen_typesent}\n**What you typed:** `{msgf}`\n**Time Taken:** {time_taken}')
        
        prLog.info(f'typetest command finished by {ctx.author} at {ctx.author.guild}')
        
    @commands.command(name='pfp', brief='Download someone\'s profile picture')
    async def pfp(self, ctx, member: discord.Member = None):
        prLog.info(f'pfp command started by {ctx.author} at {ctx.author.guild}')

        if member is None:
            member = ctx.author
        
        embed = discord.Embed(title = f"{member}'s profile picture", description = "Click on the picture to download!", colour = member.colour)
        embed.set_image(url = member.avatar.url)
        embed.set_footer(text = f"Command executed by {ctx.author}")
        await ctx.send(embed = embed)
        
        prLog.info(f'pfp command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='announce', brief='Announce a special formatted message in a channel')
    async def announce(self, ctx, channel: discord.TextChannel, *, announcement):
        prLog.info(f'announce command started by {ctx.author} at {ctx.author.guild}')

        announcement = str(announcement)
        utcrn = datetime.datetime.utcnow()
        timestamp = utcrn.strftime("Date: %d/%b/%Y | Time: %H:%M:%S UTC")

        embed = discord.Embed(title = ":loudspeaker: Announcement!", colour = ctx.author.colour)
        embed.set_footer(text = timestamp)

        embed.set_author(name = f"Announcement by {ctx.author.display_name}", icon_url = ctx.author.avatar.url)

        embed.add_field(name = "------------------", value = f"\n{announcement}\n------------------", inline = False)

        await channel.send(embed = embed)

        prLog.info(f'announce command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='whois', brief='Find information on a user')
    async def whois(self, ctx, *, member: discord.Member = None):
        prLog.info(f'whois command started by {ctx.author} at {ctx.author.guild}')

        if member is None:
            member = ctx.author

        embed = discord.Embed(
        title = 'User Information',
        description = f'User Information for {member.display_name}',
        colour = member.color
        )

        embed.set_footer(text = f'Command Executed by {ctx.author}')
        embed.set_thumbnail(url = member.avatar.url)
    
        embed.add_field(name = "Name:", value = member, inline = False)
        embed.add_field(name = "ID:", value = member.id, inline = False)
        embed.add_field(name = "Server:", value = member.guild, inline = False)
        embed.add_field(name = "Account Creation On:", value = member.created_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Joined This Server On:", value = member.joined_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Top Role:", value = member.top_role.mention, inline = False)
        embed.add_field(name = "Current Activity/Status:", value = member.activity, inline = False)
        embed.add_field(name = "Is A Bot?:", value = member.bot, inline = False)

        await ctx.send(embed = embed)
        
        prLog.info(f'whois command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='sinfo', brief='Get information on the current server')
    async def sinfo(self, ctx):
        prLog.info(f'sinfo command started by {ctx.author} at {ctx.author.guild}')

        server = ctx.author.guild
        embed = discord.Embed(
        title = 'Server Information',
        description = f'Server Information for {server.name}',
        colour = server.owner.colour
        )

        embed.set_footer(text = f'Command Executed by {ctx.author}')
        embed.set_thumbnail(url = server.icon.url)
    
        embed.add_field(name = "Name:", value = server.name, inline = False)
        embed.add_field(name = "ID:", value = server.id, inline = False)
        # embed.add_field(name = "Region:", value = server.region, inline = False)
        embed.add_field(name = "Owner:", value = server.owner, inline = False)
        embed.add_field(name = "Member Count:", value = server.member_count, inline = False)
        embed.add_field(name = "Created At:", value = server.created_at.strftime('%a %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = "Verification Level:", value = server.verification_level, inline = False)
        embed.add_field(name = "Text Channels:", value = len(server.text_channels), inline = False)
        embed.add_field(name = "Voice Channels:", value = len(server.voice_channels), inline = False)   
        embed.add_field(name = "Emojis:", value = len(server.emojis), inline = False) 

        await ctx.send(embed = embed)
        prLog.info(f'sinfo command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='clear', aliases=['cls'], brief='Clears messages', description='Clears a specified amount of messages. Takes no big than 100 messages at once.')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amt):
        prLog.info(f'clear command started by {ctx.author} at {ctx.author.guild}')

        try:
            amt = int(amt)
        except:
            await ctx.send('Only numbers allowed as argument!')
            return

        if amt > 100:
            await ctx.send('Only 100 messages at a time dude!!')
            return

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send('Are you sure to delete {} messages? (Reply with yes/y or anything else for no)'.format(amt))
        msgrecv = await self.bot.wait_for('message', check=check)

        if msgrecv.content.lower() == 'yes' or 'y':
            await ctx.channel.purge(limit=amt + 3)
            msgsent = await ctx.send('Cleared {} messages :white_check_mark:'.format(amt))
            await sleep(3)
            await msgsent.delete()

        else:
            msgsent = await ctx.send('Didn\'t touch the messages. *sigh*')
            await sleep(3)
            await msgsent.delete()

        prLog.info(f'clear command finished by {ctx.author} at {ctx.author.guild}')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send(ctx.message.channel, "Looks like you don't have the `manage_messages` permission.")
            prLog.error("recent clear command user did not have manage messages permission")
      
    '''@math.error
    async def cmd_math_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(f'debug: TRIGGER: math command (invalid_eq) triggered by {ctx.author} at {ctx.author.guild}')
            await ctx.send("That's Not A Valid Equation My Friend")
            print(f'debug: TRIGGER: math command (invalid_eq) complete at {ctx.author.guild}')'''

async def setup(bot):
    await bot.add_cog(Utilities(bot))
    prLog.debug("Plugin utilities is loaded")
