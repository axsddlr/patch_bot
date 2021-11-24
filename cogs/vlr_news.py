import os

import requests
import ujson as json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Webhook, Embed
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.global_utils import news_exists, matches_exists, flatten

load_dotenv()
vlr_news_webhook = os.getenv("vlr_news_webhook_url")
vlr_matches_webhook = os.getenv("vlr_matches_webhook_url")
crimson = 0xDC143C


def getVLRUpdates():
    URL = "https://api.axsddlr.xyz/vlr/news"
    response = requests.get(URL)
    return response.json()


def getVLRMatches():
    URL = "https://api.axsddlr.xyz/v2/vlr/match/results"
    response = requests.get(URL)
    return response.json()


class VLR_NEWS(commands.Cog, name="VLR News"):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 900})

    async def vlr_news_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "vlr_old.json"

        # call API
        responseJSON = getVLRUpdates()

        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        author = responseJSON["data"]["segments"][0]["author"]
        url = responseJSON["data"]["segments"][0]["url_path"]
        full_url = "https://www.vlr.gg" + url

        # check if file exists
        news_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, '', None)
        check_file_json = res["data"]["segments"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == title:
            # print("True")
            return
        elif check_file_json != title:
            # print("False")
            hook = Webhook(vlr_news_webhook)
            hook.send(full_url)

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    async def vlr_matches_monitor(self):
        await self.bot.wait_until_ready()

        saved_json = "vlr_matches.json"

        # call API
        responseJSON = getVLRMatches()

        team1 = responseJSON["data"][0]["team1"]["name"]
        team2 = responseJSON["data"][0]["team2"]["name"]
        score1 = responseJSON["data"][0]["team1"]["score"]
        score2 = responseJSON["data"][0]["team2"]["score"]
        flag1 = responseJSON["data"][0]["team1"]["flag"]
        flag2 = responseJSON["data"][0]["team2"]["flag"]
        ids = responseJSON["data"][0]["id"]
        time_completed = responseJSON["data"][0]["status"]
        round_info = responseJSON["data"][0]["event"]["stage"]
        tournament_name = responseJSON["data"][0]["event"]["name"]
        url = responseJSON["data"][0]["link"]
        tournament_icon = responseJSON["data"][0]["event"]["icon"]
        full_url = "https://www.vlr.gg" + url

        # check if file exists
        matches_exists(saved_json)

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, '', None)
        check_file_json = res["data"][0]["team1"]["name"]

        # compare title string from file to title string from api then overwrite file
        if check_file_json == team1:
            # print("True")
            return
        elif check_file_json != team1:
            # print("False")
            hook = Webhook(vlr_matches_webhook)

            embed = Embed(
                title=f"**VLR Match Results**",
                description=f"**{tournament_name}**\n\n[Match page]({full_url})\n\n",
                color=crimson,
                # timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text=f"{round_info} | {time_completed}")
            embed.add_field(
                name=f"__Teams__",
                value=f":{flag1}: **{team1}**\n:{flag2}: **{team2}**",
                inline=True,
            )
            embed.add_field(
                name=f"__Result__", value=f"**{score1}**\n**{score2}**", inline=True
            )
            embed.set_thumbnail(url=f"{tournament_icon}")

            hook.send(embed=embed)

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    @commands.Cog.listener()
    async def on_ready(self):

        scheduler = self.scheduler

        # add job for scheduler
        scheduler.add_job(self.vlr_matches_monitor, "interval", seconds=45)
        scheduler.add_job(self.vlr_news_monitor, "interval", minutes=30)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(VLR_NEWS(bot))
