import logging as prLog
prLog.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=prLog.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

import discord
import random
from discord.ext import commands
from time import sleep

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    objs = ["Rock","Paper","Scissors"]

    @commands.command(name='rps', brief='Play Rock Paper Scissors with the bot!')
    async def rps(self, ctx, *, question = random.choice(objs)):
        prLog.info(f'rps command started by {ctx.author} at {ctx.author.guild}')

        objs_in = ['Rock','Paper','Scissors','rock','paper','scissors','Stone','stone']
        objs = ["Rock","Paper","Scissors"]
        if question in objs_in:
            embed = discord.Embed(
                title = "Rock Paper Scissors !",
                description = f"{ctx.author.display_name} Chose {question}", 
                colour = ctx.author.colour
            )

            embed.set_footer(text = f"Command executed by {ctx.author}")
            embed.add_field(name = "----------------", value = f"Bot Chose {random.choice(objs)}", inline = False)

            await ctx.send(embed = embed)
        else:
            await ctx.send("Enter A Correct Object eg- Rock, paper, Scissors, stone.")
        
        prLog.info(f'rps command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='8ball', brief='Test your fate with the 8ball game!')
    async def _8ball(self, ctx, *, question):
        prLog.info(f'8ball command started by {ctx.author} at {ctx.author.guild}')

        answers = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
        ]

        embed = discord.Embed(
        title = "8ball",
        colour = ctx.author.colour
        )

        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        embed.set_footer(text = f"Command executed by {ctx.author}")

        embed.add_field(name = f"Question: **{question}**", value = f"Answer: **{random.choice(answers)}**")

        await ctx.send(embed = embed)

        prLog.info(f'8ball command finished by {ctx.author} at {ctx.author.guild}')

    @commands.command(name='battle', brief='Play a battle game against the bot! (Pretty dumb ngl)')
    async def battle(self, ctx):
        prLog.info(f'battle command started by {ctx.author} at {ctx.author.guild}')

        num = random.randint(0,10)
        bot_objs = random.randint(0,10)
        num = int(num)
        embed = discord.Embed(description = f"{ctx.author.display_name} launched {num} nukes, troops, armored vehicles and grenades.", colour = ctx.author.colour)
        if num > 11 :
            await ctx.send("You can use 0 to 10 objects only")
        else:
            num = str(num)
            embed.set_author(name = f"{ctx.author.display_name}'s battle game", icon_url = ctx.author.avatar_url)
            embed.set_footer(text = f"Command executed by {ctx.author}")

            embed.add_field(name = "-----------------", value = f"The enemy launched {bot_objs} nukes, troops, armored vehicles and grenades.", inline = False)
            await ctx.send(embed = embed)
            num = int(num)
            if num < bot_objs :
                await ctx.send("Can you do better next time?")
            elif num == bot_objs :
                await ctx.send("No one could survive!")
            else:
                await ctx.send("Well done, Captain!")
        
        prLog.info(f'battle command finished by {ctx.author} at {ctx.author.guild}')

    # never completed
    @commands.command(name='armwrestle', brief='Multiplayer armwrestle game! (Probably is broken)')
    async def __armwrestle__(self, ctx):
        prLog.info(f'armwrestle command started by {ctx.author} at {ctx.author.guild}')

        await ctx.send(f"**Type 'JOIN' to join {ctx.author.display_name} for armwrestling**")
        msg1 = await self.bot.wait_for('message', check = None)
        player_msgs = 0
        opponent_msgs = 0
        chosen_battle_typesent = "under development"
        if msg1.content == "JOIN" or "join" and msg1.author != ctx.author:
            await ctx.send(f"{msg1.author} is battling with {ctx.author.display_name}")
            await ctx.send(f"You both have to start typing {chosen_battle_typesent} in 3s")
            sleep(1)
            await ctx.send("2")
            sleep(1)
            await ctx.send("1")
            sleep(1)
            await ctx.send("GO!")
            while player_msgs or opponent_msgs != 3:
                msg2 = await self.bot.wait_for('message', check = None)
                if msg2.author == ctx.author:
                    player_msgs = player_msgs + 1
                elif msg2.author == msg1.author:
                    opponent_msgs = opponent_msgs + 1
                else:
                    continue
            if player_msgs == 3:
                 await ctx.send(f"**{ctx.author.display_name}** won the game. WOO! HOO!")
            elif opponent_msgs == 3:
                await ctx.send(f"**{msg1.author.display_name}** won the game. WOO! HOO!")
            else:
                await ctx.send("An error occured in the mainstream\n**ERROR CODE: _0TED**")
        else:
            pass

        prLog.info(f'armwrestle command finished by {ctx.author} at {ctx.author.guild}')

async def setup(bot):
    await bot.add_cog(Games(bot))
    prLog.debug("Plugin games is loaded")
