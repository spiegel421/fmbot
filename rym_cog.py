import discord
from discord.ext import commands
from webcrawler import retrievers
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
        
        await self.bot.say("https://www.rateyourmusic.com/~"+username)


    @rym.command(pass_context=True)
    async def set(self, ctx, username):
 #       if ctx.message.channel != self.bot.get_channel('245685218055290881'):
 #           return

        status = retrievers.check_valid_username(username)
        if "404" in status:
            await self.bot.say("That is not a valid username.")
            return

        rym_data.add_username(ctx.message.author.id, username)
        await self.bot.say("I love you.")

    @rym.command(pass_context=True)
    async def get(self, ctx):
        member = discord.utils.find(lambda m: m.name.lower() == ctx.message.content[9:].lower()
                                    or m.id in ctx.message.content, ctx.message.channel.server.members)
        if member is None:
            await self.bot.say("Sorry, this user was not found.")
            return

        username = rym_data.get_username(member.id)
        if username is None:
            await self.bot.say(member.name + " doesn't seem to have a RYM profile established.")
            return

        await self.bot.say("https://www.rateyourmusic.com/~"+username)

    @rym.command(pass_context=True)
    async def topratings(self, ctx, genre):
 #       if ctx.message.channel != self.bot.get_channel('245685218055290881'):
 #           return

        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        embed = discord.Embed(title=username+"'s top-rated "+genre+" albums")

        data = retrievers.get_top_ratings(username, genre)
        for datum in data:
            embed.add_field(name=datum['artist'], value="["+datum['album']+"]("+datum['album_link']+")")
            
        await self.bot.say(embed=embed)
        
def setup(bot):
    bot.add_cog(RYMCog(bot))
