import os
import time

import requests
import ujson as json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Webhook, Embed, File
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.global_utils import news_exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")
crimson = 0xDC143C


def getTFTGameUpdates():
    URL = "https://api.axsddlr.xyz/tft/en-us/patch_notes"
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


class TFT_Updates(commands.Cog, name="TFT Updates"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def tftupdates(self):
        await self.bot.wait_until_ready()

        # patch-notes channel
        saved_json = "tft_patch_old.json"
        responseJSON = getTFTGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"]["segments"][0]["thumbnail"]
        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        url = responseJSON["data"]["segments"][0]["url_path"]
        tag = responseJSON["data"]["segments"][0]["tag"]
        full_url = "https://teamfighttactics.leagueoflegends.com/en-us" + url
        status = responseJSON["data"]["status"]

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
        if data is not None or status == 200:
            if check_file_json == title:
                # print("not patch notes")
                return
            elif check_file_json != title:
                # print("False")
                hook = Webhook(patches_webhook)

                embed = Embed(
                    title="Teamfight Tactics",
                    description=f"[{title}]({full_url})\n\n{description}",
                    color=crimson,
                    timestamp="now",  # sets the timestamp to current time
                )
                embed.set_footer(text="Patch bot")
                embed.set_image(url=banner)
                file = File("./assets/images/tft_logo.png", name="tft_logo.png")
                embed.set_thumbnail(url="attachment://tft_logo.png")

                hook.send(embed=embed, file=file)

                f = open(saved_json, "w")
                print(json.dumps(responseJSON), file=f)

        f.close()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.tftupdates, "interval", seconds=3800)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(TFT_Updates(bot))
