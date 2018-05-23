import discord
from discord.ext import commands

class HelpCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            msg = "Use $help <cog> for help with a particular cog. Cogs are fm and rym."
            await self.bot.say(msg)

    @help.command()
    async def fm(self):
        line1 = "last.fm commands.\n"
        line2 = "$fm: displays your last played track.\n"
        line3 = "$fm set <username>: sets your last.fm username.\n"
        line4 = "$fm topartists: displays your top artists on last.fm.\n"
        line5 = "$fm trendingartists <num_days>: displays server's top artists in past num_days."

        await self.bot.say(line1 + line2 + line3 + line4 + line5)

def setup(bot):
    bot.add_cog(HelpCog(bot))
