import discord
from discord.ext import commands
from webcrawler import retrievers
import rym_data
import time

class RYMCog:
    def __init__(self, bot):
        self.bot = bot
        self.topratings_msgs = {}

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
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return

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
    async def topratings(self, ctx, genre=''):
 #       if ctx.message.channel != self.bot.get_channel('245685218055290881'):
 #           return
        
        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        ctx.genre = genre
        await commands.Command.invoke(self.embed_top_ratings, ctx)
    
    @commands.command(pass_context=True)
    @commands.cooldown(1, 180, commands.BucketType.channel)
    async def embed_top_ratings(self, ctx):
        username = rym_data.get_username(ctx.message.author.id)
        
        page = 0
        description = ""
        data = retrievers.get_top_ratings(username, ctx.genre, page)
        if len(data) == 0:
            await self.bot.say("Either that is not a genre or you have rated no albums from it.")
            return
        for datum in data[:5]:
            description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"

        embed = discord.Embed(title=username+"'s top-rated "+ctx.genre.replace("+", " ")+" albums", description=description)
        embed.set_footer(text="Page " + str(page+1))
        msg = await self.bot.say(embed=embed)

        self.topratings_msgs[msg.id] = (ctx.message.author, ctx.genre, page, data)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id not in self.topratings_msgs:
            return
        elif user is reaction.message.author:
            return

        await self.flip_page(reaction, reaction.message, reaction.message.id)

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id not in self.topratings_msgs:
            return
        elif user is reaction.message.author:
            return

        await self.flip_page(reaction, reaction.message, reaction.message.id)

    async def flip_page(self, reaction, msg, msg_id):
        author = self.topratings_msgs[msg_id][0]
        genre = self.topratings_msgs[msg_id][1]
        page = self.topratings_msgs[msg_id][2]
        data = self.topratings_msgs[msg_id][3]
        username = rym_data.get_username(author.id)

        if reaction.emoji == '➡':
            page += 1
            n = page % 5
            if n == 0:
                data = retrievers.get_top_ratings(username, genre, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s top-rated "+genre.replace("+", " ")+" albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            n = page % 5
            if n == 4:
                data = retrievers.get_top_ratings(username, genre, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s top-rated "+genre.replace("+", " ")+" albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.topratings_msgs[msg_id] = (author, genre, page, data)
        await self.bot.edit_message(msg, embed=embed)

    @embed_top_ratings.error
    async def embed_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.message.author.id == '387046431262769153':
                await self.bot.say('Frawg, more like, mug lite')
            else:
                await self.bot.say("Wait {}m, {}s for the cooldown, love.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
        else:
            await self.bot.say("Unknown error occurred. <@359613794843885569>, darling, get your shit straight.")
        
def setup(bot):
    bot.add_cog(RYMCog(bot))
