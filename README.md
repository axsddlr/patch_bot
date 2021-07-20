# Rehkbot

Personal Discord bot

## Requirements

- Python 3.6 and up - https://www.python.org/downloads/
- git - https://git-scm.com/download/

### How to install modules

```
for windows:
python -m pip install -r requirements.txt

for linux:
python3 -m pip install -r requirements.txt
```

### Required Linux Packages

Run shell script located in root directory:

`./setup.sh -i`

Required packages to make bot run efficiently:

```
python3-psutil
python3-dbus
ffmpeg

```

### ENV

rename `.env.example` to `.env` then store your token and some other private info like this:

```
DISCORD_TOKEN =
DISCORD_BOT_ID =
```

### .ENV (for Twitch Live Notifier)

In your `.env` fill in this info:

```
STREAMER=
Image_Priority=Game
TWITCH_CLIENT_ID =
TWITCH_CLIENT_SECRET =
WEBHOOK_URL =
Message =
Description =

```

### PM2

PM2 is an alternative script provided by NodeJS, which will reboot your bot whenever it crashes and keep it up with a nice status. You can install it by doing `npm install -g pm2` and you should be done.

```
# Start the bot
pm2 start pm2.json

# Tips on common commands
pm2 <command> [name]
  start discordbot.py    Run the bot again if it's offline
  list                    Get a full list of all available services
  stop discordbot.py     Stop the bot
  reboot discordbot.py   Reboot the bot
```
