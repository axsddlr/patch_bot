import os
import time
import ujson as json
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from dhooks import Webhook, Embed, File
from utils.global_utils import news_exists, matches_exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")
crimson = 0xDC143C

def getLOLGameUpdates():
    URL = "https://api.axsddlr.xyz/lol/patch_notes"
    response = requests.get(URL)
    return response.json()


def updater(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            updater(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


class LOL_Updates(commands.Cog, name="LOL Updates"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def lolupdates(self):
        await self.bot.wait_until_ready()

        # patch-notes channel
        saved_json = "lol_patch_old.json"
        responseJSON = getLOLGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"]["segments"][0]["thumbnail"]
        title = responseJSON["data"]["segments"][0]["title"]
        url = responseJSON["data"]["segments"][0]["url"]

        # check if file exists
        news_exists(saved_json)

        time.sleep(5)

        # open saved_json file
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"]["segments"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(patches_webhook)

            embed = Embed(
                title="League of Legends",
                description=f"[{title}]({url})\n\n",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")
            embed.set_image(url=banner)
            file = File(
                "./assets/images/league_of_legends_sm.png",
                name="league_of_legends_sm.png",
            )
            embed.set_thumbnail(url="attachment://league_of_legends_sm.png")

            hook.send(embed=embed, file=file)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.lolupdates, "interval", seconds=3700)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(LOL_Updates(bot))
