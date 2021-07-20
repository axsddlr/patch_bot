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
reddit_webhook = os.getenv("reddit_webhook_url")
crimson = 0xDC143C


def getValorantGameUpdates():
    URL = "https://api.axsddlr.xyz/valorant/news/en-us/game-updates"
    response = requests.get(URL)
    return response.json()

def getVALREDUpdates():
    URL = "https://api.axsddlr.xyz/reddit/Valorant"
    response = requests.get(URL, headers=headers)
    return response.json()


def updater(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            updater(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


class Valorant_Updates(commands.Cog, name="Valorant Updates"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def valupdates(self):
        await self.bot.wait_until_ready()

        # patch-notes channel
        saved_json = "valo_patch_old.json"
        responseJSON = getValorantGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"]["segments"][0]["thumbnail"]
        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        url = responseJSON["data"]["segments"][0]["url_path"]
        external_link = responseJSON["data"]["segments"][0]["external_link"]

        if external_link == "":
            full_url = "https://playvalorant.com/en-us" + url
        else:
            full_url = external_link

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
                title="VALORANT",
                description=f"[{title}]({full_url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Rehkbot")
            embed.set_image(url=banner)
            file = File(
                "./assets/images/valorant_sm.png",
                name="valorant_sm.png",
            )
            embed.set_thumbnail(url="attachment://valorant_sm.png")

            hook.send(embed=embed, file=file)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    async def reddit_monitor(self):
        await self.bot.wait_until_ready()

        # call API
        # patch-notes channel
        saved_json = "reddit_old.json"
        responseJSON = getVALREDUpdates()

        basetree = responseJSON["data"]["segments"][0]

        title = basetree["title"]
        thumbnail = basetree["thumbnail_url"]
        url_path = basetree["url_path"]
        author = basetree["author"]
        # description = basetree["selftext"]
        flair = basetree["flair"]
        full_url = "https://www.reddit.com" + url_path

        # check if file exists
        news_exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"]["segments"][0]["title"]

        if (flair != "Educational") and (check_file_json == title):
            # print("not patch notes")
            return
        elif (flair == "Educational") and (check_file_json != title):
            # print("False")
            hook = Webhook(reddit_webhook)

            embed = Embed(
                title="VALORANT REDDIT",
                description=f"[{title}]({full_url})\n\n author: {author}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/val_reddit.png", name="val_reddit.png")
            embed.set_thumbnail(url="attachment://val_reddit.png")

            hook.send(embed=embed, file=file)
            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()


    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.valupdates, "interval", seconds=3600)
        scheduler.add_job(self.reddit_monitor, "interval", seconds=900)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(Valorant_Updates(bot))
