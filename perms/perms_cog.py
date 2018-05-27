import discord
from discord.ext import commands
import perms.perms_data

class PermsCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def perms(self, ctx):
        if ctx.message.author.id != '359613794843885569':
            return
        if ctx.invoked_subcommand is None:
            return

    @perms.command()
    async def allow(self, channel_id, cog):
        if cog == "fm" or cog == "rym":
            perms_data.remove_disallow(channel_id[2:20], cog)

    @perms.command()
    async def disallow(self, channel_id, cog):
        if cog == "fm" or cog == "rym":
            perms_data.add_disallow(channel_id[2:20], cog)

def setup(bot):
    bot.add_cog(PermsCog(bot))
