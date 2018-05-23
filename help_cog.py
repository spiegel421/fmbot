import discord
from discord.ext import commands

class HelpCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def help(self, ctx, command):
        if ctx.invoked_subcommand is not None:
            return

        line1 = "`For info on bot cogs, type $help <cog>.\n`"
        line2 = "`$fm: cog relating to your lastfm account.\n`"
        line3 = "`$rym: cog relating to your RYM account.`"

        await self.bot.say(line1+line2+line3)

def setup(bot):
    bot.add_cog(HelpCog(bot))
