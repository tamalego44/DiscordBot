import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
from discord.ext import commands


client_id = os.getenv('DISCORD_CLIENT_ID')
endpoint = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())