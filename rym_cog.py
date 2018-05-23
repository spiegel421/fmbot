import discord
from discord.ext import commands
import webcrawler
import rym_data

class RYMCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def rym(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        embed = discord.Embed(colour=0x000080, title=ctx.message.author.nick+"'s RYM profile", description="https://www.rateyourmusic.com/~"+username)
        await self.bot.say(embed=embed)


    @rym.command(pass_context=True)
    async def set(self, ctx, username):
 #       if ctx.message.channel != self.bot.get_channel('245685218055290881'):
 #           return

        rym_data.add_username(ctx.message.author.id, username)
        await self.bot.say("I love you.")
        
def setup(bot):
    bot.add_cog(RYMCog(bot))
