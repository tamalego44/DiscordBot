from dotenv import load_dotenv
from discord.ext import commands
#from discord.voice_client import VoiceClient
import discord
import requests
import random
import os
import traceback
import hashlib
from gtts import gTTS
import os   
from youtube import YTDLSource
from sclib import SoundcloudAPI, Track
from discord.ext import commands
import traceback
import db
# import DiscordBot.WIP.cod as cod
# from DiscordBot.WIP.db import CSVDB
# db = CSVDB()

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

def download(fileUrl, filename, channel):
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
            print("Downloading file: " + fileUrl)

    return path + '/' + hash

queues = {}
async def playsong(ctx: commands.Context, source, name, filename):
    server = ctx.message.guild
    voice_channel = server.voice_client

    db.insert(str(server.id), filename, name, ctx.author.id)

    if voice_channel.is_playing():
        if server.id not in queues:
            queues[server.id] = []
        queues[server.id].append((source, name))
        await ctx.send(f'Added {name}. \n **{len(queues[server.id])}** in queue.')
    else:
        server.voice_client.play(source, after=lambda x=0: check_queue(ctx))
        await ctx.send('**Now playing:** {}'.format(name))

def check_queue(ctx: commands.Context):
    server = ctx.message.guild
    if server.id in queues and len(queues[server.id]):
        source, name = queues[server.id].pop(0)
        server.voice_client.play(source, after=lambda x=0: check_queue(ctx))
        #await ctx.send('**Now playing:** {}'.format(name)) TODO: Fix this
    else:
        voice_client = ctx.message.guild.voice_client
        voice_client.stop()



@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx: commands.Context):
    if not ctx.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice or voice.channel != channel:
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send("Connected to {}'s voice channel".format(ctx.message.author.name))

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx: commands.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

valid_filetypes = ["mp3"]
@bot.command(name='play', help="This command plays a file")
async def play(ctx, url: str = None):
    try:
        await join(ctx)
        if ctx.message.attachments:
            for file in ctx.message.attachments:
                if file.filename.split(".")[-1] in valid_filetypes:
                    async with ctx.typing():
                        filename = download(''.join(file.url), file.filename, str(ctx.message.channel))
                        await playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), file.filename.split(".")[0], filename)
                else:
                    await ctx.send("%s is not of a supported filetype. Supported filetypes: %s" % (file.filename, valid_filetypes))
        elif url and url.startswith("https://soundcloud.com"):
            #Soundcloud Player
            print(url)
            async with ctx.typing():
                api = SoundcloudAPI()
                track = api.resolve(url)
                assert type(track) is Track
                filename = f'./temp/{track.artist} - {track.title}.mp3'
                if not os.path.exists(filename):
                    with open(filename, 'wb+') as file:
                        track.write_mp3_to(file)
                await playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), f"{track.artist} - {track.title}", filename)
        elif url:
            #TODO: Only allow youtube links
            print(url)
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=bot.loop)
                await playsong(ctx, player, f'{player.title}', player.filename)
        else:
            await ctx.send("Play... what? Send a file or a link.")
    except Exception:
        print(traceback.format_exc())
        await ctx.send("Something went wrong. Notify <@186322107783839746>")


voice_filename = 'temp.mp3'
@bot.command(name='say', help='Habiba will say a command')
async def say(ctx: commands.Context, *text: str):
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
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filepath))
        except Exception as e:
            traceback.print_exc()
            await ctx.send("The bot is not connected to a voice channel.")
        
        #engine.stop()


@bot.command(name='pause', help='This command pauses the current song. Resume playing with !resume')
async def pause(ctx: commands.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song that was paused with !pause')
async def resume(ctx: commands.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use !play command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx: commands.Context):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='loop', help='Toggle looping for the current song')
async def loop(ctx: commands.Context):
    await ctx.send("this function is not yet supported")

valid_filetypes = ["mp3"]
@bot.command(name='replay', help="Replay a previous song")
async def play(ctx, index: int = -1):
    try:
        await join(ctx)
        rec = db.get(str(ctx.message.guild.id), index)
        await playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=rec[1]), "TEMP VALUE", rec[1])
    except Exception:
        print(traceback.format_exc())
        await ctx.send("Something went wrong. Notify <@186322107783839746>")


bot.run(TOKEN)
