import discord
import time
import psutil
import os
import datetime
from discord.ext import commands

start_time = time.time()


class InfoCog(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.2)

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f"{member.display_name} joined on {member.joined_at}")

    @commands.command(name="ping", help="check if bot is working")
    @commands.has_any_role(236267540777533440)
    async def ping(self, ctx):
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["botinvite"])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(
            f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.bot.user.id)}>"
        )

    @commands.command(aliases=["info"])
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        ramUsage = self.process.memory_full_info().rss / 1024 ** 2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(
            # crimson color code
            colour=(0xDC143C)
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name=("Uptime"), value=(text), inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(
            name="Servers",
            value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )",
            inline=True,
        )
        embed.add_field(
            name="# of Commands",
            value=len([x.name for x in self.bot.commands]),
            inline=True,
        )
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **`1.0.0`**", embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.


def setup(bot):
    bot.add_cog(InfoCog(bot))
