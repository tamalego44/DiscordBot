client_id = 1042601465526624276
endpoint = 'https://discord.com/api/oauth2/authorize?client_id=1042601465526624276&permissions=8&scope=bot'

# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class MyClient(discord.Client):
    async def on_ready(self):
        #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        self.print_members(guild)

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Welcome to the shitshow, {member.name}.'
        )

    def print_members(self, guild):
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    async def on_message(self, message):
        if message.author == client.user:
            return

        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        if message.content == '99!':
            response = random.choice(brooklyn_99_quotes)
            await message.channel.send(response)
        elif message.content == 'raise-exception':
            self.channel = message.channel
            raise discord.DiscordException
        

    async def on_error(self, event, *args, **kwargs):
        await self.channel.send(f'Unhandled message: {args[0]}\n')

        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise

intents = discord.Intents.all()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)