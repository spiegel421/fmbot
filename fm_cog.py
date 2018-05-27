import discord
from discord.ext import commands
import fm_data, perms_data
import time
from lastfmwrapper import LastFmWrapper

class FmCog:
    def __init__(self, bot):
        self.bot = bot
        self.topartist_msgs = {}
        self.trendingartist_msgs = {}
        self.lastfm = LastFmWrapper()
    
    @commands.group(pass_context=True)
    async def fm(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        elif perms_data.get_disallowed(ctx.message.channel.id, "fm"):
            return
        
        username = fm_data.get_username(ctx.message.author.id)
        if username == None:
            await self.bot.say("Set a username first. It's ok, bud, we all make mistakes sometimes.")
            return
        
        last_played = self.lastfm.get_last_played(username)
        if last_played == None:
            await self.bot.say(username + " has never played any songs.")
            return

        await commands.Command.invoke(self.embed_now_playing, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def embed_now_playing(self, ctx):
        username = fm_data.get_username(ctx.message.author.id)
        now_playing = self.lastfm.get_last_played(username)
        artist = now_playing.artist.name
        artist_search_url = "["+artist+("](https://rateyourmusic.com/search?&searchtype=a&searchterm="+artist+")").replace(" ","%20")
        track = now_playing.title
        embed = discord.Embed(colour=0xFF0000, title=track, description=artist_search_url)
        embed.set_author(name=username, icon_url=ctx.message.author.avatar_url, url="https://www.last.fm/user/" + username)
        embed.set_thumbnail(url=now_playing.image)
        
        await self.bot.say(embed=embed)

        scrobble_data = {
            'discord_id': ctx.message.author.id,
            'lastfm_username': username,
            'artist': artist,
            'track': track,
            'timestamp': time.time(),
        }
        fm_data.add_scrobble_data(scrobble_data)

    @fm.command(pass_context=True)
    async def scrobbles(self, ctx, *args):
        username = fm_data.get_username(ctx.message.author.id)
        if username == None:
            await self.bot.say("Set a username first. It's ok, bud, we all make mistakes sometimes.")
            return

        artist_name = ""
        for value in *args:
            artist_name += value + " "
        artist_name = artist_name[:-1]

        play_count = str(self.lastfm.get_user_numscrobbles(username, artist_name))
        await self.bot.say(ctx.message.author.name+" has scrobbled "+artist_name+" "+play_count+" times.")

    @fm.command(pass_context=True)
    async def trendingartists(self, ctx, num_days):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        trending_artist_dict = fm_data.find_trending_artists(int(num_days))
        sorted_dict = sorted(trending_artist_dict.items(), key=lambda x: x[1], reverse=True)

        ctx.trending_artists = sorted_dict
        await commands.Command.invoke(self.embed_trending_artists, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.channel)
    async def embed_trending_artists(self, ctx):
        page = 0
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            if i > len(ctx.trending_artists) - 1:
                break
            artist_search_url = "["+ctx.trending_artists[i][0]+("](https://rateyourmusic.com/search?&searchtype=a&searchterm="+ctx.trending_artists[i][0]+")").replace(" ","%20")
            description += artist_search_url + "\n"
        embed = discord.Embed(colour=0x000080, title="Server's trending artists", description=description)
        embed.set_footer(text="Page " + str(page+1))

        msg = await self.bot.say(embed=embed)
        self.trendingartist_msgs[msg.id] = (ctx.trending_artists, page)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    @fm.command(pass_context=True)
    async def set(self, ctx, username):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        if self.lastfm.get_user(username) is None:
            await self.bot.say("User not found. I'm sure you'll get it right eventually. <3")
            return

        fm_data.add_username(ctx.message.author.id, username)
        await self.bot.say("I love you.")

    @fm.command(pass_context=True)
    async def topartists(self, ctx):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        username = fm_data.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Set a username first. It's ok, bud, we all make mistakes sometimes.")
            return

        wrapper = self.lastfm.get_user_artists(username)
        if wrapper.total_artists == 0:
            await self.bot.say(username + " has not played any artists.")
            return

        await commands.Command.invoke(self.embed_top_artists, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def embed_top_artists(self, ctx):
        username = fm_data.get_username(ctx.message.author.id)
        wrapper = self.lastfm.get_user_artists(username)
        top_artists = wrapper.artists
        if wrapper.total_artists > 10:
            top_artists = top_artists[:10]
            
        page = 0
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
        embed = discord.Embed(colour=0x228B22, description=description)
        embed.set_author(name=username + "'s top artists", url="https://www.last.fm/user/" + username)
        embed.set_footer(text="Page " + str(page+1))
        
        msg = await self.bot.say(embed=embed)
        self.topartist_msgs[msg.id] = (ctx.message.author, page)
        await self.bot.add_reaction(msg, '⬅')
        await self.bot.add_reaction(msg, '➡')

    async def on_reaction_add(self, reaction, user):
        if (reaction.message.id not in self.topartist_msgs and reaction.message.id not in self.trendingartist_msgs):
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topartist_msgs:
            await self.flip_page_top(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.trendingartist_msgs:
            await self.flip_page_trending(reaction, reaction.message, reaction.message.id)

    async def on_reaction_remove(self, reaction, user):
        if (reaction.message.id not in self.topartist_msgs and reaction.message.id not in self.trendingartist_msgs):
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topartist_msgs:
            await self.flip_page_top(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.trendingartist_msgs:
            await self.flip_page_trending(reaction, reaction.message, reaction.message.id)

    async def flip_page_top(self, reaction, msg, msg_id):
        author = self.topartist_msgs[msg_id][0]
        page = self.topartist_msgs[msg_id][1]
        username = fm_data.get_username(author.id)
        wrapper = self.lastfm.get_user_artists(username)
        top_artists = wrapper.artists
        max_pages = wrapper.total_artists / 10 + 1

        if reaction.emoji == '➡' and page < max_pages - 1:
            page += 1
            description = ""
            for i in range(page * 10, (page + 1) * 10):
                if i > wrapper.total_artists - 1:
                    break
                description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
            embed = discord.Embed(colour=0x228B22, description=description)
            embed.set_author(name=username + "'s top artists", url="https://www.last.fm/user/" + username)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            description = ""
            for i in range(page * 10, (page + 1) * 10):
                if i > wrapper.total_artists - 1:
                    break
                description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
            embed = discord.Embed(colour=0x228B22, description=description)
            embed.set_author(name=username + "'s top artists", url="https://www.last.fm/user/" + username)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.topartist_msgs[msg_id] = (author, page)
        await self.bot.edit_message(msg, embed=embed)

    async def flip_page_trending(self, reaction, msg, msg_id):
        trending_artists = self.trendingartist_msgs[msg_id][0]
        page = self.trendingartist_msgs[msg_id][1]
        max_pages = int(len(trending_artists) / 10 + 1)

        if reaction.emoji == '➡' and page < max_pages - 1:
            page += 1
            description = ""
            for i in range(page * 10, (page + 1) * 10):
                if i > len(trending_artists) - 1:
                    break
                artist_search_url = "["+trending_artists[i][0]+("](https://rateyourmusic.com/search?&searchtype=a&searchterm="+trending_artists[i][0]+")").replace(" ","%20")
                description += artist_search_url + "\n"
            embed = discord.Embed(colour=0x000080, title="Server's trending artists", description=description)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            description = ""
            for i in range(page * 10, (page + 1) * 10):
                if i > len(trending_artists) - 1:
                    break
                artist_search_url = "["+trending_artists[i][0]+("](https://rateyourmusic.com/search?&searchtype=a&searchterm="+trending_artists[i][0]+")").replace(" ","%20")
                description += artist_search_url + "\n"
            embed = discord.Embed(colour=0x000080, title="Server's trending artists", description=description)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.trendingartist_msgs[msg_id] = (trending_artists, page)
        await self.bot.edit_message(msg, embed=embed)
        
    @embed_now_playing.error
    @embed_top_artists.error
    @embed_trending_artists.error
    async def embed_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.message.author.id == '387046431262769153':
                await self.bot.say('Frawg, more like, mug lite')
            else:
                await self.bot.say("Wait {}m, {}s for the cooldown, love.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
        else:
            await self.bot.say("Unknown error occurred. <@359613794843885569>, darling, get your shit straight.")

def setup(bot):
    bot.add_cog(FmCog(bot))
