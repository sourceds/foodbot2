import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

prefix = '미식봇! '
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.run(TOKEN)
