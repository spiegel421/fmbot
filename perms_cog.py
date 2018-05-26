import discord
from discord.ext import commands
import perms_data

class PermsCog:
    def __init__(self, bot):
        self.bot = bot

#    def is_owner(self, ctx):
#        return ctx.author.id == '359613794843885569'

    @commands.group(pass_context=True)
#    @commands.is_owner()
    async def perms(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @perms.command()
    async def allow(self, channel_id, cog):
        perms_data.remove_disallow(channel_id[2:20], cog)

    @perms.command()
    async def disallow(self, channel_id, cog):
        perms_data.add_disallow(channel_id[2:20], cog)

def setup(bot):
    bot.add_cog(PermsCog(bot))
