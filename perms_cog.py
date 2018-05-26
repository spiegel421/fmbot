import discord
from discord.ext import commands
import perms_data

class PermsCog:
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(self, ctx):
        return ctx.author.id == '359613794843885569'

    @commands.group(pass_context=True)
    @commands.check(is_owner)
    async def perms(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @perms.command()
    async def allow(self, channel, cog):
        perms_data.remove_disallow(channel.id, cog)

    @perms.command()
    async def disallow(self, channel, cog):
        perms_data.add_disallow(channel.id, cog)

def setup(bot):
    bot.add_cog(PermsCog(bot))