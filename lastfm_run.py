import discord
from discord.ext import commands
import scrobbles, trending, usernames
import scrapy
from scrapy.crawler import CrawlerProcess
import genrecrawl
import time, random
from lastfmwrapper import LastFmWrapper

bot = commands.Bot(command_prefix='$')
lastfm = LastFmWrapper()
topartist_msgs = {}
trendingartist_msgs = {}
process = CrawlerProcess()
genre_spider = genrecrawl.GenrecrawlSpider()

@bot.group(pass_context=True)
async def fm(ctx):
    if ctx.invoked_subcommand is not None:
        return
    
    username = usernames.get_username(ctx.message.author.id)
    if username == None:
        await bot.say("Set a username first. Bitch.")
        return
    
    last_played = lastfm.get_last_played(username)
    if last_played == None:
        await bot.say(username + " has never played any songs.")
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
    
    await bot.say(embed=embed)

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
    if ctx.message.channel != bot.get_channel('245685218055290881'):
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

    msg = await bot.say(embed=embed)
    trendingartist_msgs[msg.id] = (ctx.trending_artists, page)
    await bot.add_reaction(msg, '⬅')
    await bot.add_reaction(msg, '➡')

@fm.command(pass_context=True)
async def set(ctx, username):
    if ctx.message.channel != bot.get_channel('245685218055290881'):
        return
    
    if lastfm.get_user(username) is None:
        await bot.say("User not found. Try learning how to type.")
        return

    usernames.add_username(ctx.message.author.id, username)
    await bot.say("Username set. You should feel proud of yourself.")

@fm.command(pass_context=True)
async def topartists(ctx):
    if ctx.message.channel != bot.get_channel('245685218055290881'):
        return
    
    username = usernames.get_username(ctx.message.author.id)
    if username is None:
        await bot.say("Set a username first. Bitch.")
        return

    wrapper = lastfm.get_user_artists(username)
    if wrapper.total_artists == 0:
        await bot.say(username + " has not played any artists.")
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
    
    msg = await bot.say(embed=embed)
    topartist_msgs[msg.id] = (ctx.message.author, page)
    await bot.add_reaction(msg, '⬅')
    await bot.add_reaction(msg, '➡')

@bot.event
async def on_reaction_add(reaction, user):
    if (reaction.message.id not in topartist_msgs and reaction.message.id not in trendingartist_msgs):
        return
    elif user is reaction.message.author:
        return

    if reaction.message.id in topartist_msgs:
        await flip_page_top(reaction, reaction.message, reaction.message.id)
    elif reaction.message.id in trendingartist_msgs:
        await flip_page_trending(reaction, reaction.message, reaction.message.id)

@bot.event
async def on_reaction_remove(reaction, user):
    if (reaction.message.id not in topartist_msgs and reaction.message.id not in trendingartist_msgs):
        return
    elif user is reaction.message.author:
        return

    if reaction.message.id in topartist_msgs:
        await flip_page_top(reaction, reaction.message, reaction.message.id)
    elif reaction.message.id in trendingartist_msgs:
        await flip_page_trending(reaction, reaction.message, reaction.message.id)

async def flip_page_top(reaction, msg, msg_id):
    author = topartist_msgs[msg_id][0]
    page = topartist_msgs[msg_id][1]
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

    topartist_msgs[msg_id] = (author, page)
    await bot.edit_message(msg, embed=embed)

async def flip_page_trending(reaction, msg, msg_id):
    trending_artists = trendingartist_msgs[msg_id][0]
    page = trendingartist_msgs[msg_id][1]
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

    trendingartist_msgs[msg_id] = (trending_artists, page)
    await bot.edit_message(msg, embed=embed)
    
@embed_now_playing.error
@embed_top_artists.error
@embed_trending_artists.error
async def embed_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say("Wait {}m, {}s for the cooldown, you neanderthal.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
    else:
        await bot.say("Unknown error occurred. <@359613794843885569>, get your shit straight.")

@bot.command()
async def genres(artist, album):
    genre_spider.start_urls = ['https://rateyourmusic.com/release/album/'+artist+'/'+album+'/']
    
    process.crawl(genre_spider)
    process.start()
    
    reader = open("genres.txt", 'r')
    pri_genres = reader.readline().split("\t")
    sec_genres = reader.readline().split("\t")
    reader.close()
    
    msg = ""
    for i in range(len(pri_genres)):
        msg += pri_genres[i]
        if i < len(pri_genres) - 2:
            msg += ", "
    for i in range(len(sec_genres)):
        msg += sec_genres[i]
        if i < len(sec_genres) - 2:
            msg += ", "

    await bot.say(msg)
    
bot.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
