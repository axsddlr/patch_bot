import os

import requests
import ujson as json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Webhook, Embed, File
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.global_utils import nww_exists, flatten

load_dotenv()
nww_webhook = os.getenv("patches_webhook_url")
crimson = 0xDC143C


def getNWWUpdatesV1():
    URL = "https://api.axsddlr.xyz/newworld/news/updates"
    response = requests.get(URL)
    return response.json()


def getNWWUpdatesV2():
    URL = "https://api.axsddlr.xyz/newworld/forums/notice"
    response = requests.get(URL)
    return response.json()


def getNWWUpdatesV3():
    URL = "https://api.axsddlr.xyz/newworld/forums/updates"
    response = requests.get(URL)
    return response.json()


def getNWWREDUpdates():
    URL = "https://api.axsddlr.xyz/reddit/Newworld"
    response = requests.get(URL)
    return response.json()


class NWW_Patch(commands.Cog, name="New World Patch Notes"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 800})

    async def nww_patch_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_old.json"

        # call API
        responseJSON = getNWWUpdatesV1()

        title = responseJSON["data"][0]["title"]
        description = responseJSON["data"][0]["description"]
        thumbnail = responseJSON["data"][0]["thumbnail"]
        url = responseJSON["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, '', None)
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
                description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    async def nww_patch_monitorv2(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_old_2.json"

        # call API
        responseJSON = getNWWUpdatesV2()

        title = responseJSON["data"][0]["title"]
        # description = responseJSON["data"][0]["description"]
        thumbnail = "https://images.ctfassets.net/j95d1p8hsuun/12Tl0sQL6vNRfXPkIrfuaz" \
                    "/2374cc44fec67de6b53bcc080a57345d/keyart2.jpg "
        url = responseJSON["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, '', None)
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
                title="New World Forums",
                description=f"[{title}]({url})\n\n\n",
                # description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    async def nww_patch_monitorv3(self):
        await self.bot.wait_until_ready()

        saved_json = "nww_old_3.json"

        # call API
        responseJSON = getNWWUpdatesV3()

        title = responseJSON["data"][0]["title"]
        # description = responseJSON["data"][0]["description"]
        thumbnail = "https://images.ctfassets.net/j95d1p8hsuun/12Tl0sQL6vNRfXPkIrfuaz" \
                    "/2374cc44fec67de6b53bcc080a57345d/keyart2.jpg "
        url = responseJSON["data"][0]["url"]

        # check if file exists
        nww_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, '', None)
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
                title="New World Forums",
                description=f"[{title}]({url})\n\n\n",
                # description=f"[{title}]({url})\n\n{description}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/nw_logo.png", name="nw_logo.png")
            embed.set_thumbnail(url="attachment://nw_logo.png")

            hook.send(embed=embed, file=file)

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.nww_patch_monitor, "interval", minutes=30)
        scheduler.add_job(self.nww_patch_monitorv2, "interval", minutes=31)
        scheduler.add_job(self.nww_patch_monitorv3, "interval", minutes=32)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(NWW_Patch(bot))
