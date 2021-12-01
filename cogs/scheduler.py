from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nextcord.ext import commands

from utils.esports.vlr_news import VLR_NEWS
from utils.games.leagueoflegends import LOL_Updates
from utils.games.new_world_news import NWW_Patch
from utils.games.teamfighttactics import TFT_Updates
from utils.games.valorant import Valorant_Updates


class job_scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 200})
        self.vlrnews = VLR_NEWS()
        self.valorant = Valorant_Updates()
        self.lol = LOL_Updates()
        self.nw = NWW_Patch()
        self.tft = TFT_Updates()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add jobs for scheduler

        # valorant news monitor
        scheduler.add_job(self.vlrnews.vlr_news_monitor, "interval", minutes=30)

        # valorant matches monitor
        scheduler.add_job(self.vlrnews.vlr_matches_monitor, "interval", seconds=45)

        # valorant updates monitor
        scheduler.add_job(self.valorant.valupdates, "interval", minutes=60)

        # valorant reddit monitor
        scheduler.add_job(self.valorant.valorant_monitor, "interval", minutes=20)

        # valorant comp reddit monitor
        scheduler.add_job(self.valorant.valorant_comp_monitor, "interval", minutes=25)

        # League of Legends patch notes monitor
        scheduler.add_job(self.lol.lolupdates, "interval", minutes=30)

        # League of Legends patch monitor
        scheduler.add_job(self.nw.nww_patch_monitor, "interval", minutes=30)

        # New World forums monitor
        scheduler.add_job(self.nw.nww_patch_monitorv2, "interval", minutes=31)
        scheduler.add_job(self.nw.nww_patch_monitorv3, "interval", minutes=32)

        # TFT patch notes monitor
        scheduler.add_job(self.tft.tftupdates, "interval", minutes=31)

        # starting the scheduler
        scheduler.start()


def setup(bot):
    bot.add_cog(job_scheduler(bot))
