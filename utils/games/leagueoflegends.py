import os

import requests
import ujson as json
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv
from utils.global_utils import crimson, flatten, news_exists

load_dotenv()
patches_webhook = os.getenv("patches_webhook_url")


def getLOLGameUpdates():
    URL = "https://api.axsddlr.xyz/lol/en-us/patch_notes"
    response = requests.get(URL)
    return response.json()


class LOL_Updates:
    async def lolupdates(self):

        # patch-notes channel
        saved_json = "lol_patch_old.json"
        responseJSON = getLOLGameUpdates()

        # JSON Results Mapping
        banner = responseJSON["data"]["segments"][0]["thumbnail"]
        title = responseJSON["data"]["segments"][0]["title"]
        description = responseJSON["data"]["segments"][0]["description"]
        url_path = responseJSON["data"]["segments"][0]["url_path"]
        full_url = "https://na.leagueoflegends.com" + url_path
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
                # print("True")
                return
            elif check_file_json != title:
                # print("False")
                hook = Webhook(patches_webhook)

                embed = Embed(
                    title="League of Legends",
                    description=f"[{title}]({full_url})\n\n{description}",
                    color=crimson,
                    timestamp="now",  # sets the timestamp to current time
                )
                embed.set_footer(text="Patch Bot")
                embed.set_image(url=banner)
                file = File(
                    "./assets/images/league_of_legends_sm.png",
                    name="league_of_legends_sm.png",
                )
                embed.set_thumbnail(url="attachment://league_of_legends_sm.png")

                hook.send(embed=embed, file=file)

                with open(saved_json, "w") as updated:
                    json.dump(responseJSON, updated, ensure_ascii=False)

                updated.close()
