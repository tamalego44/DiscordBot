# DiscordBot
Habiba the Discord Bot

## To fix YT-DLP problem
python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
import yt_dlp as youtube_dl

## TODO
- Make all user feedback more uniform
- Improve help messages
- Add help info to bot profile
- Add !skip or !next cmd (TESTING)
- Add !last command (TESTING)
- Have habiba remove herself from queue when appropriate https://stackoverflow.com/questions/63658589/how-to-make-a-discord-bot-leave-the-voice-channel-after-being-inactive-for-x-min
- Add way for user to see queue (TESTING)
- Habiba says whats coming next in queue
- Expand valid filetypes
- Gambling...
- organization https://stackoverflow.com/questions/50678419/how-to-make-multiple-files-python-bot
- Logging https://discordpy.readthedocs.io/en/latest/logging.html

## Bug List
- Variable Bit-Rate mp3s are not handled properly by ffmpeg
    - https://stackoverflow.com/questions/10437750/how-to-get-the-real-actual-duration-of-an-mp3-file-vbr-or-cbr-server-side
    - [mp3 @ 0x1e07900] Estimating duration from bitrate, this may be inaccurate
- 