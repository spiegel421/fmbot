import discord, scrobbles, time
from discord.ext import commands
from lastfmwrapper import LastFmWrapper

bot = commands.Bot(command_prefix='$')
lastfm = LastFmWrapper()

def read_username_file(username_dict):
    reader = open("usernames.txt", 'r')
    lines = reader.readlines()
    for line in lines:
        author = line.split(",")[0]
        username = line.split(",")[1]
        username = username[:-1]
        if lastfm.get_user(username) != None:
            username_dict[author] = username
    reader.close()

def rewrite_username_file(username_dict):
    writer = open("usernames.txt", 'w')
    for author, username in username_dict.items():
        writer.write(author + "," + username + "\n")
    writer.close()
    
username_dict = {}
read_username_file(username_dict)
topartist_msgs = {}

@bot.group(pass_context=True)
async def fm(ctx):
    if ctx.invoked_subcommand is not None:
        return
    
    author = str(ctx.message.author)
    if author not in username_dict:
        await bot.say("Set a username first. Bitch.")
        return
    
    username = username_dict[author]
    last_played = lastfm.get_last_played(username)
    if last_played == None:
        await bot.say(username + " has never played any songs.")
        return

    await commands.Command.invoke(embed_now_playing, ctx)

@fm.command(pass_context=True)
async def set(ctx, username):
    author = str(ctx.message.author)
    if lastfm.get_user(username) is None:
        await bot.say("User not found. Try learning how to type.")
        return
    
    username_dict[author] = username
    rewrite_username_file(username_dict)
    await bot.say("Username set. You should feel proud of yourself.")

@commands.command(pass_context=True)
@commands.cooldown(1, 420, commands.BucketType.user)
async def embed_now_playing(ctx):
    author = str(ctx.message.author)
    username = username_dict[author]
    now_playing = lastfm.get_last_played(username)
    artist = now_playing.artist.name
    artist_search_url = "["+artist+("](https://rateyourmusic.com/search?&searchtype=a&searchterm="+artist+")").replace(" ","%20")
    track = now_playing.title
    embed = discord.Embed(colour=0xFF0000, title=track, description=artist_search_url)
    embed.set_author(name=username, icon_url=ctx.message.author.avatar_url, url="https://www.last.fm/user/" + username)
    embed.set_thumbnail(url=now_playing.image)
    
    await bot.say(embed=embed)

    scrobble_data = {
        'discord_user': author,
        'lastfm_username': username,
        'artist': artist,
        'track': track,
        'timestamp': time.time(),
    }
    scrobbles.add_scrobble_data(scrobble_data)

@fm.command(pass_context=True)
async def topartists(ctx):
    if ctx.message.channel != bot.get_channel('245685218055290881'):
        return
    
    author = str(ctx.message.author)
    if author not in username_dict:
        await bot.say("Set a username first. Bitch.")
        return

    username = username_dict[author]
    wrapper = lastfm.get_user_artists(username)
    if wrapper.total_artists == 0:
        await bot.say(username + " has not played any artists.")
        return

    await commands.Command.invoke(embed_top_artists, ctx)

@commands.command(pass_context=True)
@commands.cooldown(1, 420, commands.BucketType.user)
async def embed_top_artists(ctx):
    author = str(ctx.message.author)
    username = username_dict[author]
    wrapper = lastfm.get_user_artists(username)
    top_artists = wrapper.artists
    if wrapper.total_artists > 10:
        top_artists = top_artists[:10]
        
    page = 0
    description = ""
    for i in range(page * 10, (page + 1) * 10):
        description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
    embed = discord.Embed(colour=0xFF0000, description=description)
    embed.set_footer(text="Page " + str(page+1))
    
    msg = await bot.say(embed=embed)
    topartist_msgs[msg.id] = (author, page)
    await bot.add_reaction(msg, '⬅')
    await bot.add_reaction(msg, '➡')

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.id not in topartist_msgs or user is reaction.message.author:
        return

    author = topartist_msgs[reaction.message.id][0]
    page = topartist_msgs[reaction.message.id][1]
    username = username_dict[author]
    wrapper = lastfm.get_user_artists(username)
    top_artists = wrapper.artists

    if reaction.emoji == '➡':
        page += 1
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
        embed = discord.Embed(colour=0xFF0000, description=description)
        embed.set_footer(text="Page " + str(page+1))

        topartist_msgs[reaction.message.id] = (author, page)
        await bot.edit_message(reaction.message, embed=embed)
    elif reaction.emoji == '⬅' and page > 0:
        page -= 1
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
        embed = discord.Embed(colour=0xFF0000, description=description)
        embed.set_footer(text="Page " + str(page+1))

        topartist_msgs[reaction.message.id] = (author, page)
        await bot.edit_message(reaction.message, embed=embed)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.id not in topartist_msgs or user is reaction.message.author:
        return

    author = topartist_msgs[reaction.message.id][0]
    page = topartist_msgs[reaction.message.id][1]
    username = username_dict[author]
    wrapper = lastfm.get_user_artists(username)
    top_artists = wrapper.artists

    if reaction.emoji == '➡':
        page += 1
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
        embed = discord.Embed(colour=0xFF0000, description=description)
        embed.set_footer(text="Page " + str(page+1))

        topartist_msgs[reaction.message.id] = (author, page)
        await bot.edit_message(reaction.message, embed=embed)
    elif reaction.emoji == '⬅' and page > 0:
        page -= 1
        description = ""
        for i in range(page * 10, (page + 1) * 10):
            description += "[**" + top_artists[i].name + "**](" + top_artists[i].url + ") (" + str(top_artists[i].play_count) + ")\n"
        embed = discord.Embed(colour=0xFF0000, description=description)
        embed.set_footer(text="Page " + str(page+1))

        topartist_msgs[reaction.message.id] = (author, page)
        await bot.edit_message(reaction.message, embed=embed)
    
@embed_now_playing.error
@embed_top_artists.error
async def embed_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say("Wait {}m, {}s for the cooldown, you neanderthal.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
    else:
        await bot.say(error)

bot.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
