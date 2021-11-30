import os

import nextcord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.esports.vlr_news import VLR_NEWS
from utils.games.leagueoflegends import LOL_Updates
from utils.games.new_world_news import NWW_Patch
from utils.games.teamfighttactics import TFT_Updates
from utils.games.valorant import Valorant_Updates

vlrnews = VLR_NEWS()
valorant = Valorant_Updates()
lol = LOL_Updates()
nw = NWW_Patch()
tft = TFT_Updates()


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ["$"]

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return "?"

    # allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")

# This is what we're going to use to load the cogs on startup
if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                # This will load it
                bot.load_extension("cogs.{0}".format(filename[:-3]))
                # this is to let us know which cogs got loaded
                print("{0} is online".format(filename[:-3]))
            except:
                print("{0} was not loaded".format(filename))
                continue


@bot.event
async def on_ready():
    # change presence to display custom message
    await bot.change_presence(activity=nextcord.Game(name="$help"))

    scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 200})

    # add jobs for scheduler

    # valorant news monitor
    scheduler.add_job(vlrnews.vlr_news_monitor, "interval", minutes=30)

    # valorant matches monitor
    scheduler.add_job(vlrnews.vlr_matches_monitor, "interval", seconds=45)

    # valorant updates monitor
    scheduler.add_job(valorant.valupdates, "interval", minutes=60)

    # valorant reddit monitor
    scheduler.add_job(valorant.valorant_monitor, "interval", minutes=20)

    # valorant comp reddit monitor
    scheduler.add_job(valorant.valorant_comp_monitor, "interval", minutes=25)

    # League of Legends patch notes monitor
    scheduler.add_job(lol.lolupdates, "interval", minutes=30)

    # League of Legends patch monitor
    scheduler.add_job(nw.nww_patch_monitor, "interval", minutes=30)

    # New World forums monitor
    scheduler.add_job(nw.nww_patch_monitorv2, "interval", minutes=31)
    scheduler.add_job(nw.nww_patch_monitorv3, "interval", minutes=32)

    # TFT patch notes monitor
    scheduler.add_job(tft.tftupdates, "interval", minutes=31)

    # starting the scheduler
    scheduler.start()

    print("Bot connected")


bot.run(TOKEN, reconnect=True)
