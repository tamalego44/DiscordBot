import asyncio
import hashlib
import os
import discord
import requests
import yt_dlp as youtube_dl

"""
MUSIC FUNCTIONALITY FUNCTIONS
"""
class Song(object):
    def __init__(self, ctx, source, name, filename):
        self.source = source
        self.name = name
        self.filename = filename
        self.uploader = ctx.author

fileDirectory = './temp/'
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

""""
YOUTUBE_DL FUNCTIONS
"""
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'temp/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, filename, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.filename = filename

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename, **ffmpeg_options), data=data, filename=filename)
    
