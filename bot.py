from dotenv import load_dotenv
from discord.ext import commands
import discord
import string
import requests
import random
import os
import traceback
import hashlib
from gtts import gTTS
import os   

import cod
from db import CSVDB
db = CSVDB()

client_id = 1042601465526624276
endpoint = 'https://discord.com/api/oauth2/authorize?client_id=1042601465526624276&permissions=8&scope=bot'
fileDirectory = './temp/'

# bot.py

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

def download(fileUrl, filename, channel):
    print("Downloading file: " + fileUrl)
    path = fileDirectory + channel
    fileDownload = requests.get(fileUrl)

    BLOCKSIZE = 65536
    hasher = hashlib.sha256()
    # for i in range(0, fileDownload.content, BLOCKSIZE):
    #     hasher.update(fileDownload.content[i:i+BLOCKSIZE])
    hasher.update(fileDownload.content)
    hash = hasher.hexdigest()

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isfile(path + '/' + hash):     
        with open(path + '/' + hash, 'wb') as file:
            file.write(fileDownload.content)

    return path + '/' + hash

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

valid_filetypes = ["mp3"]
@bot.command(name='play', help="This command plays a file")
async def play(ctx, url = None):
    # voice_client = ctx.message.guild.voice_client
    # if not voice_client.is_connected():
    #     channel = ctx.message.author.voice.channel
    #     await channel.connect()

    await join(ctx)
    
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            if file.filename.split(".")[-1] in valid_filetypes:
                filename = download(''.join(file.url), file.filename, str(ctx.message.channel))

                try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        voice_channel.play(discord.FFmpegPCMAudio(executable="./ffmpeg", source=filename))
                    await ctx.send('**Now playing:** {}'.format(file.filename))
                except Exception as e:
                    traceback.print_exc()
                    await ctx.send("The bot is not connected to a voice channel.")
            else:
                await ctx.send("%s is not of a supported filetype. Supported filetypes: %s" % (file.filename, valid_filetypes))
    else:
        ## Check if its a link
        #if url =
        pass 

    # else:
    #     try :
    #         server = ctx.message.guild
    #         voice_channel = server.voice_client
    #         async with ctx.typing():
    #             filename = await YTDLSource.from_url(url, loop=bot.loop)
    #             voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    #         await ctx.send('**Now playing:** {}'.format(filename))
    #     except:
    #         await ctx.send("The bot is not connected to a voice channel.")

# async def sayWords(ctx, text):



voice_filename = 'temp.mp3'
@bot.command(name='say', help='Habiba will say a command')
async def say(ctx, *text: str):
    if text:
        
        path = fileDirectory + str(ctx.message.guild)
        tts = gTTS(text=' '.join(text), lang='en')#, tld='com.au')
        tts.save(voice_filename)

        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        with open(voice_filename, 'rb') as f:
            while True:
                data = f.read(BLOCKSIZE)
                if not data:
                    break
                hasher.update(data)
        hash = hasher.hexdigest()

        filepath = path + '/' + hash

        if not os.path.exists(path):
            os.makedirs(path)
       
        os.replace(voice_filename, filepath)

        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            #async with ctx.typing():
            voice_channel.play(discord.FFmpegPCMAudio(executable="./ffmpeg", source=filepath))
        except Exception as e:
            traceback.print_exc()
            await ctx.send("The bot is not connected to a voice channel.")
        
        #engine.stop()



@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# setcod command
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        command = message.content.split(' ')

        if command[0] == 'setcod':
            user_id = str(message.author.id)
            name = command[1]
            succ = db.insert(user_id, name)
            if succ:
                await message.channel.send('Successfully registered your COD name as %s' % name)
            else:
                await message.channel.send('Failed to register your cod name. Blame James.')
    
    await bot.process_commands(message)

# @bot.command()
# async def DM(ctx, user: discord.User, *, name: str):
#     print('trigger')
#     user_id = str(user.id)
#     succ = db.insert(user_id, name)
#     if succ:
#         await user.send('Successfully registered your COD name as %s' % name)
#     else:
#         await user.send('Failed to register your cod name. Blame James.')

@bot.command(name='kd', help='Display your MW KD. Send a message <setcod (name#12345)> to Habiba to register.')
async def kd(ctx):
    ## 1 Get the users info
    user_id = str(ctx.message.author.id)
    name = db.get(user_id)

    if not name:
        await ctx.send('I don\'t know your Activision ID. Send me a message with the format "setcod username#12345" to set your id')
    else:
        kd = await cod.get_kd(name)
        if kd < 0.9:
            emoji = ':regional_indicator_l:'
        elif kd < 1.1:
            emoji = ':face_with_diagonal_mouth:'
        else:
            emoji = ':peanuts:'
            
        await ctx.send('Your KD in MW is %0.2f %s' % (kd, emoji))

bot.run(TOKEN)


# TODO: expand valid filetypes
# TODO: Play should connect you to the server
# TODO: allow fixing cod name