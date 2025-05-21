import discord
from discord.ext import commands, tasks
import random
import asyncio
import os
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Currency storage - simple dict, for demo
user_cash = {}
user_daily = {}

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command()
async def help(ctx):
    help_text = """
    Commands:
    !help - Show this message
    !info - Bot info
    !ccash - Show your cashia balance
    !hunt - Hunt a creature to earn cashia
    !daily - Claim your daily cashia (24h cooldown)
    """
    await ctx.send(help_text)

@bot.command()
async def info(ctx):
    await ctx.send("This is your awesome Discord bot with cashia currency!")

@bot.command()
async def ccash(ctx):
    user = ctx.author.id
    cash = user_cash.get(user, 0)
    await ctx.send(f"{ctx.author.mention}, you have {cash} cashia.")

@bot.command()
async def hunt(ctx):
    user = ctx.author.id
    creatures = ["rabbit", "deer", "bear", "dragon"]
    caught = random.choice(creatures)
    earned = random.randint(10, 50)
    user_cash[user] = user_cash.get(user, 0) + earned
    await ctx.send(f"{ctx.author.mention} hunted a {caught} and earned {earned} cashia!")

@bot.command()
async def daily(ctx):
    user = ctx.author.id
    now = datetime.utcnow()
    last_claim = user_daily.get(user)

    if last_claim and now - last_claim < timedelta(hours=24):
        remaining = timedelta(hours=24) - (now - last_claim)
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"{ctx.author.mention}, you already claimed your daily. Try again in {hours}h {minutes}m.")
    else:
        reward = 100
        user_cash[user] = user_cash.get(user, 0) + reward
        user_daily[user] = now
        await ctx.send(f"{ctx.author.mention}, you claimed your daily {reward} cashia!")

# Run the bot with token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
