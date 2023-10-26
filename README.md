# DiscordBot
My Discord Bot

## To fix YT-DLP problem
python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
import yt_dlp as youtube_dl

## TODO
- Make all user feedback more uniform
- Improve help messages
- Add help info to bot profile
- Add !skip or !next cmd
- Add !last command
- Have habiba remove herself from queue when appropriate
- Add way for user to see queue
- Habiba says whats coming next in queue
- Expand valid filetypes
- Gambling...

## Bug List
- Variable Bit-Rate mp3s are not handled properly by ffmpeg
    - https://stackoverflow.com/questions/10437750/how-to-get-the-real-actual-duration-of-an-mp3-file-vbr-or-cbr-server-side
    - [mp3 @ 0x1e07900] Estimating duration from bitrate, this may be inaccurate
- 