import os
import time

import requests
import ujson as json
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv
from utils.global_utils import crimson, flatten, news_exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")


def getTFTGameUpdates():
    URL = "https://api.axsddlr.xyz/tft/en-us/patch_notes"
    response = requests.get(URL)
    return response.json()


class TFT_Updates:
    async def tftupdates(self):

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

        # open saved_json file
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
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

                with open(saved_json, "w") as updated:
                    json.dump(responseJSON, updated, ensure_ascii=False)

                updated.close()
