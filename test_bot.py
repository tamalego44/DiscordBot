import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

client_id = os.getenv('DISCORD_CLIENT_ID')
endpoint = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot'
fileDirectory = './temp/'

# bot.py

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

cog_files = ['commands.test1', 'commands.test2']

for cog_file in cog_files:
    bot.load_extension(cog_file)
    print("%s has loaded" % cog_file)