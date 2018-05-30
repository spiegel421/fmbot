"""
The RYM cog; controls all RYM-related commands. Uses scrapy webcrawler to fetch data from RYM, and displays it in embeds.

"""
import discord
from discord.ext import commands
from webcrawler import retrievers
import rym_data, perms_data
import time

with open("server_index.txt", 'r') as reader:
    SERVER_INDEX = int(reader.read())

class RYMCog:
    def __init__(self, bot):
        self.bot = bot
        self.topratings_msgs = {}
        self.aoty_msgs = {}
        self.recent_msgs = {}
        self.time_last_crawled = 0
        self.cooldown_time = 30
        self.current_server = 0

    # Check function for a hard 30-second throttle on all RYM commands that crawl the site.
    def check_cooled_down(self):
        return time.time() - self.time_last_crawled < self.cooldown_time

    # If no subcommand was invoked, retrieves RYM username from database and displays it.
    @commands.group(pass_context=True)
    async def rym(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        elif perms_data.get_disallowed(ctx.message.channel.id, "rym"):
            return

        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return
        
        await self.bot.say("https://www.rateyourmusic.com/~"+username)

    # Sets RYM username, first checking if the username is valid and case-sensitive
    # (as case-insensitive redirects can be harmful to important queries later on).   
    @rym.command(pass_context=True)
    async def set(self, ctx, username):
        self.current_server = (self.current_server + 1) % 1
        if self.current_server != SERVER_INDEX:
            return
        if self.check_cooled_down():
            for x in self.bot.get_all_emojis():
                if x.id == '449250117833457680':
                    await self.bot.add_reaction(ctx.message, str(x))
            return
        self.time_last_crawled = time.time()

        status = retrievers.check_valid_username(username)
        if "404" in status or "302" in status or "303" in status:
            await self.bot.say("That is not a valid username. (Remember that usernames are case sensitive.)")
            return

        rym_data.add_username(ctx.message.author.id, username)
        await self.bot.say("I love you.")

    # Gets the RYM username of another user, either by mention or by search.
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
        self.current_server = (self.current_server + 1) % 1
        if self.current_server != SERVER_INDEX:
            return
        
        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        if self.check_cooled_down():
            for emoji in self.bot.get_all_emojis():
                if emoji.id == '449250117833457680':
                    await self.bot.add_reaction(ctx.message, str(x))
            return
        self.time_last_crawled = time.time()

        ctx.genre = genre
        await commands.Command.invoke(self.embed_top_ratings, ctx)
    
    @commands.command(pass_context=True)
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

        self.topratings_msgs[msg.id] = (username, ctx.genre, page, data)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    @rym.command(pass_context=True)
    async def aoty(self, ctx, year=''):
        self.current_server = (self.current_server + 1) % 1
        if self.current_server != SERVER_INDEX:
            return
        
        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        if self.check_cooled_down():
            return
        self.time_last_crawled = time.time()

        ctx.year = year
        await commands.Command.invoke(self.embed_aoty, ctx)
    
    @commands.command(pass_context=True)
    async def embed_aoty(self, ctx):
        username = rym_data.get_username(ctx.message.author.id)
        
        page = 0
        description = ""
        data = retrievers.get_aoty(username, ctx.year, page)
        if len(data) == 0:
            await self.bot.say("Either that is not a year or you have rated no albums from it.")
            return
        for datum in data[:5]:
            description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"

        embed = discord.Embed(title=username+"'s top-rated "+(ctx.year if ctx.year != '' else '2018')+" albums", description=description)
        embed.set_footer(text="Page " + str(page+1))
        msg = await self.bot.say(embed=embed)

        self.aoty_msgs[msg.id] = (username, ctx.year, page, data)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    @rym.command(pass_context=True)
    async def recent(self, ctx):
        self.current_server = (self.current_server + 1) % 1
        if self.current_server != SERVER_INDEX:
            return
        
        username = rym_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Looks like you don't have a username set!")
            return

        if self.check_cooled_down():
            return
        self.time_last_crawled = time.time()

        await commands.Command.invoke(self.embed_recent, ctx)
    
    @commands.command(pass_context=True)
    async def embed_recent(self, ctx):
        username = rym_data.get_username(ctx.message.author.id)
        
        page = 0
        description = ""
        data = retrievers.get_recent(username, page)
        if len(data) == 0:
            await self.bot.say("Either that is not a year or you have rated no albums from it.")
            return
        for datum in data[:5]:
            description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"

        embed = discord.Embed(title=username+"'s recently rated albums", description=description)
        embed.set_footer(text="Page " + str(page+1))
        msg = await self.bot.say(embed=embed)

        self.recent_msgs[msg.id] = (username, page, data)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id not in self.topratings_msgs and reaction.message.id not in self.aoty_msgs and reaction.message.id not in self.recent_msgs:
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topratings_msgs:
            await self.flip_page_topratings(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.aoty_msgs:
            await self.flip_page_aoty(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.recent_msgs:
            await self.flip_page_recent(reaction, reaction.message, reaction.message.id)

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id not in self.topratings_msgs and reaction.message.id not in self.aoty_msgs and reaction.message.id not in self.recent_msgs:
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topratings_msgs:
            await self.flip_page_topratings(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.aoty_msgs:
            await self.flip_page_aoty(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.recent_msgs:
            await self.flip_page_recent(reaction, reaction.message, reaction.message.id)

    async def flip_page_topratings(self, reaction, msg, msg_id):
        username = self.topratings_msgs[msg_id][0]
        genre = self.topratings_msgs[msg_id][1]
        page = self.topratings_msgs[msg_id][2]
        data = self.topratings_msgs[msg_id][3]

        if reaction.emoji == '➡':
            page += 1
            n = page % 5
            if n == 0:
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
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
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
                data = retrievers.get_top_ratings(username, genre, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s top-rated "+genre.replace("+", " ")+" albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.topratings_msgs[msg_id] = (username, genre, page, data)
        await self.bot.edit_message(msg, embed=embed)

    async def flip_page_aoty(self, reaction, msg, msg_id):
        username = self.aoty_msgs[msg_id][0]
        year = self.aoty_msgs[msg_id][1]
        page = self.aoty_msgs[msg_id][2]
        data = self.aoty_msgs[msg_id][3]

        if reaction.emoji == '➡':
            page += 1
            n = page % 5
            if n == 0:
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
                data = retrievers.get_aoty(username, year, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s top-rated "+(year if year != '' else '2018')+" albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            n = page % 5
            if n == 4:
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
                data = retrievers.get_aoty(username, year, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s top-rated "+(year if year != '' else '2018')+" albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.aoty_msgs[msg_id] = (username, year, page, data)
        await self.bot.edit_message(msg, embed=embed)

    async def flip_page_recent(self, reaction, msg, msg_id):
        username = self.recent_msgs[msg_id][0]
        page = self.recent_msgs[msg_id][1]
        data = self.recent_msgs[msg_id][2]

        if reaction.emoji == '➡':
            page += 1
            n = page % 5
            if n == 0:
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
                data = retrievers.get_recent(username, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s recently rated albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            n = page % 5
            if n == 4:
                self.current_server = (self.current_server + 1) % 1
                if self.current_server != SERVER_INDEX:
                    return
                if self.check_cooled_down():
                    return
                self.time_last_crawled = time.time()
                data = retrievers.get_recent(username, page)
            description = ""
            for datum in data[5 * n:5 * (n + 1)]:
                description += "["+datum['artist']+"](https://www.rateyourmusic.com"+datum['artist_link']+") - ["+datum['album']+"](https://www.rateyourmusic.com"+datum['album_link']+") ("+datum['rating']+")\n"
            embed = discord.Embed(title=username+"'s recently rated albums", description=description)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.recent_msgs[msg_id] = (username, page, data)
        await self.bot.edit_message(msg, embed=embed)

    @embed_top_ratings.error
    @embed_aoty.error
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
