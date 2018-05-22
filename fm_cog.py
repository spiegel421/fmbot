import discord
from discord.ext import commands
import scrobbles, trending, usernames
import time
from lastfmwrapper import LastFmWrapper

class FmCog:
    def __init__(self, bot):
        self.bot = bot
        self.topartist_msgs = {}
        self.trendingartist_msgs = {}
    
    @commands.group(pass_context=True)
    async def fm(ctx):
        if ctx.invoked_subcommand is not None:
            return
        
        username = usernames.get_username(ctx.message.author.id)
        if username == None:
            await self.bot.say("Set a username first. Bitch.")
            return
        
        last_played = lastfm.get_last_played(username)
        if last_played == None:
            await self.bot.say(username + " has never played any songs.")
            return

        await commands.Command.invoke(embed_now_playing, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def embed_now_playing(ctx):
        username = usernames.get_username(ctx.message.author.id)
        now_playing = lastfm.get_last_played(username)
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
        scrobbles.add_scrobble_data(scrobble_data)


    @fm.command(pass_context=True)
    async def trendingartists(ctx, num_days):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        trending_artist_dict = trending.find_trending_artists(int(num_days))
        sorted_dict = sorted(trending_artist_dict.items(), key=lambda x: x[1], reverse=True)

        ctx.trending_artists = sorted_dict
        await commands.Command.invoke(embed_trending_artists, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.channel)
    async def embed_trending_artists(ctx):
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
    async def set(ctx, username):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        if lastfm.get_user(username) is None:
            await self.bot.say("User not found. Try learning how to type.")
            return

        usernames.add_username(ctx.message.author.id, username)
        await self.bot.say("Username set. You should feel proud of yourself.")

    @fm.command(pass_context=True)
    async def topartists(ctx):
        if ctx.message.channel != self.bot.get_channel('245685218055290881'):
            return
        
        username = usernames.get_username(ctx.message.author.id)
        if username is None:
            await self.bot.say("Set a username first. Bitch.")
            return

        wrapper = lastfm.get_user_artists(username)
        if wrapper.total_artists == 0:
            await self.bot.say(username + " has not played any artists.")
            return

        await commands.Command.invoke(embed_top_artists, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def embed_top_artists(ctx):
        username = usernames.get_username(ctx.message.author.id)
        wrapper = lastfm.get_user_artists(username)
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

    async def on_reaction_add(reaction, user):
        if (reaction.message.id not in self.topartist_msgs and reaction.message.id not in self.trendingartist_msgs):
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topartist_msgs:
            await flip_page_top(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.trendingartist_msgs:
            await flip_page_trending(reaction, reaction.message, reaction.message.id)

    async def on_reaction_remove(reaction, user):
        if (reaction.message.id not in self.topartist_msgs and reaction.message.id not in self.trendingartist_msgs):
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.topartist_msgs:
            await flip_page_top(reaction, reaction.message, reaction.message.id)
        elif reaction.message.id in self.trendingartist_msgs:
            await flip_page_trending(reaction, reaction.message, reaction.message.id)

    async def flip_page_top(reaction, msg, msg_id):
        author = self.topartist_msgs[msg_id][0]
        page = self.topartist_msgs[msg_id][1]
        username = usernames.get_username(author.id)
        wrapper = lastfm.get_user_artists(username)
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

    async def flip_page_trending(reaction, msg, msg_id):
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
    async def embed_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await self.bot.say("Wait {}m, {}s for the cooldown, you neanderthal.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
        else:
            await self.bot.say("Unknown error occurred. <@359613794843885569>, get your shit straight.")

def setup(bot):
    bot.add_cog(FmCog(bot))
