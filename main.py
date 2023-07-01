#import
import discord
from  dotenv import load_dotenv
import os
from discord.ext import commands
import time
import schedule

# .env
load_dotenv()

# discord
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

bot.run(os.getenv('TOKEN'))