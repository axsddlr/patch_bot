import discord
import requests
import os
import ujson as json
import time
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dhooks import Webhook, Embed, File
from utils.global_utils import news_exists, nww_exists

load_dotenv()
nww_webhook = os.getenv("patches_webhook_url")
crimson = 0xDC143C


def getNWWUpdatesV1():
    URL = "https://api.axsddlr.xyz/newworld/v1/updates"
    response = requests.get(URL)
    return response.json()

def getNWWUpdatesV2():
    URL = "https://api.axsddlr.xyz/newworld/v2/downtime"
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


class NWW_Patch(commands.Cog, name="New World Patch Notes"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 800})

    async def nww_patch_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_old.json"

        # call API
        responseJSON = getNWWUpdatesV1()

        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        thumbnail = responseJSON["data"]["segments"][0]["thumbnail"]
        url = responseJSON["data"]["segments"][0]["url"]

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

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            # hook = Webhook(nww_webhook)
            # hook.send(full_url)

            hook = Webhook(nww_webhook)

            embed = Embed(
                title="New World",
                description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()

    async def nww_patch_monitorv2(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_old_2.json"

        # call API
        responseJSON = getNWWUpdatesV2()

        title = responseJSON["data"][0]["title"]
        # description = responseJSON["data"][0]["description"]
        thumbnail = "https://images.ctfassets.net/j95d1p8hsuun/12Tl0sQL6vNRfXPkIrfuaz/2374cc44fec67de6b53bcc080a57345d/keyart2.jpg"
        url = responseJSON["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        time.sleep(5)
        # open saved_json and check title string
        f = open(
            saved_json,
        )
        data = json.load(f)
        res = updater(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            # hook = Webhook(nww_webhook)
            # hook.send(full_url)

            hook = Webhook(nww_webhook)

            embed = Embed(
                title="New World",
                description=f"[{title}]({url})\n\n",
                # description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            f = open(saved_json, "w")
            print(json.dumps(responseJSON), file=f)

        f.close()


    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.nww_patch_monitor, "interval", seconds=1800)
        scheduler.add_job(self.nww_patch_monitorv2, "interval", seconds=1805)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(NWW_Patch(bot))