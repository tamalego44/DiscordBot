import asyncio
import os
import traceback
import discord
import db
from discord.ext import commands
from util import download, Song, YTDLSource
from sclib import SoundcloudAPI, Track

class MusicCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {}
        self.valid_filetypes = ["mp3"]
        self.timeout = 300
    
    @commands.command(name="pause", help="This command pauses the current song. Resume playing with !resume")
    async def pause(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song that was paused with !pause')
    async def resume(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use !play command")

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='stop', help='stops playing and empties queue')
    async def stop(self, ctx: commands.Context):
        server = ctx.message.guild
        self.queues[server.id] = []
        await self.skip(ctx)

    @commands.command(name='loop', help='Toggle looping for the current song')
    async def loop(self, ctx: commands.Context):
        await ctx.send("this function is not yet supported")

    @commands.command(name='replay', help="Replay a previous song")
    async def play(self, ctx: commands.Context, index: int = -1):
        try:
            await self.join(ctx)
            rec = db.get(str(ctx.message.guild.id), index)
            await self.playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=rec[1]), "TEMP VALUE", rec[1])
        except Exception:
            print(traceback.format_exc())
            await ctx.send("Something went wrong. Notify <@186322107783839746>")

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx: commands.Context):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @commands.command(name='queue', help='Display the current queue')
    async def queue(self, ctx: commands.Context):
        server = ctx.message.guild   
        if server.id in self.queues and len(self.queues[server.id]) > 0:
            queue = self.queues[server.id]
            ret = ""
            for i, song_obj in enumerate(queue, start=1):
                ret += "%d: %s\n" % (i, song_obj.name)
            await ctx.send(ret)
        else:
            await ctx.send("Nothing in queue") # TODO: bad

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return False
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice or voice.channel != channel:
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            await ctx.send("Connected to {}'s voice channel".format(ctx.message.author.name))
        return True
    
    def check_queue(self, ctx: commands.Context):
        server = ctx.message.guild
        if server.id in self.queues and len(self.queues[server.id]):
            song_obj = self.queues[server.id].pop(0)
            server.voice_client.play(song_obj.source, after=lambda x=0: self.check_queue(ctx))
            #await ctx.send('**Now playing:** {}'.format(name)) TODO: Fix this
        else:
            voice_client = ctx.message.guild.voice_client
            voice_client.stop()

    @commands.command(name='play', help="This command plays a file")
    async def play(self, ctx: commands.Context, url: str = None):
        try:
            if not await self.join(ctx):
                return False
            
            if ctx.message.attachments:
                for file in ctx.message.attachments:
                    if file.filename.split(".")[-1] in self.valid_filetypes:
                        async with ctx.typing():
                            filename = download(''.join(file.url), file.filename, str(ctx.message.channel))
                            await self.playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), file.filename.split(".")[0], filename)
                    else:
                        await ctx.send("%s is not of a supported filetype. Supported filetypes: %s" % (file.filename, self.valid_filetypes))
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
                    await self.playsong(ctx, discord.FFmpegPCMAudio(executable="ffmpeg", source=filename), f"{track.artist} - {track.title}", filename)
            elif url:
                #TODO: Only allow youtube links
                print(url)
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.client.loop)
                    await self.playsong(ctx, player, f'{player.title}', player.filename)
            else:
                await ctx.send("Play... what? Send a file or a link.")
        except Exception:
            print(traceback.format_exc())
            await ctx.send("Something went wrong. Notify <@186322107783839746>")

    async def playsong(self, ctx: commands.Context, source, name, filename):
        server = ctx.message.guild
        voice_channel = server.voice_client

        song_obj = Song(ctx, source, name, filename)

        db.insert(str(server.id), song_obj)

        if voice_channel.is_playing():
            if server.id not in self.queues:
                self.queues[server.id] = []
            self.queues[server.id].append(song_obj)
            await ctx.send(f'Added {name}. \n **{len(self.queues[server.id])}** in queue.')
        else:
            server.voice_client.play(source, after=lambda x=0: self.check_queue(ctx))
            await ctx.send('**Now playing:** {}'.format(name))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if not member.id == self.client.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == self.timeout:
                    await voice.disconnect()
                if not voice.is_connected():
                    break

async def setup(client):
    await client.add_cog(MusicCog(client))