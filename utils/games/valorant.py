import os
import time

import requests
import ujson as json
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv
from utils.global_utils import crimson, flatten, news_exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")
reddit_webhook = os.getenv("reddit_webhook_url")


def getValorantGameUpdates():
    URL = "https://api.axsddlr.xyz/valorant/en-us/patch-notes"
    response = requests.get(URL)
    return response.json()


def getVALREDUpdates():
    URL = "https://api.axsddlr.xyz/reddit/Valorant"
    response = requests.get(URL)
    return response.json()


def getVALCOMPREDUpdates():
    URL = "https://api.axsddlr.xyz/reddit/ValorantComp"
    response = requests.get(URL)
    return response.json()


class Valorant_Updates:
    async def valupdates(self):

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
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
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

            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    async def valorant_monitor(self):

        # call API
        # patch-notes channel
        saved_json = "valorant_old.json"
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

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
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
            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()

    async def valorant_comp_monitor(self):

        # call API
        # patch-notes channel
        saved_json = "valorant_comp_old.json"
        responseJSON = getVALCOMPREDUpdates()

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

        # open saved_json and check title string
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"]["segments"][0]["title"]

        if (flair != "Highlight | Esports") and (check_file_json == title):
            # print("not patch notes")
            return
        elif (flair == "Highlight | Esports") and (check_file_json != title):
            # print("False")
            hook = Webhook(reddit_webhook)

            embed = Embed(
                title="VALORANT ESPORTS HIGHLIGHTS",
                description=f"[{title}]({full_url})\n\n author: {author}",
                color=crimson,
                timestamp="now",  # sets the timestamp to current time
            )
            embed.set_footer(text="Patch bot")
            embed.set_image(url=thumbnail)
            file = File("./assets/images/val_reddit.png", name="val_reddit.png")
            embed.set_thumbnail(url="attachment://val_reddit.png")

            hook.send(embed=embed, file=file)
            with open(saved_json, "w") as updated:
                json.dump(responseJSON, updated, ensure_ascii=False)

            updated.close()
