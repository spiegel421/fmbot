import discord
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

class UsernameNotSetError(Exception):
    def __init__(self):
        Exception.__init__(self)

class NoHistoryError(Exception):
    def __init__(self):
        Exception.__init__(self)

class UserNotFoundError(Exception):
    def __init__(self):
        Exception.__init__(self)
    
username_dict = {}
read_username_file(username_dict)

@commands.command(pass_context=True)
@commands.cooldown(1, 420, commands.BucketType.user)
async def embed(ctx):
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

@bot.command(pass_context=True)
async def fm(ctx):
    author = str(ctx.message.author)
    if author not in username_dict:
        await bot.say("Set a username first. Bitch.")
        return
    
    username = username_dict[author]
    last_played = lastfm.get_last_played(username)
    if last_played == None:
        await bot.say(username + " has never played any songs.")
        return

    await commands.Command.invoke(embed, ctx)

@bot.command(pass_context=True)
async def fmset(ctx, username):
    author = str(ctx.message.author)
    if lastfm.get_user(username) is None:
        await bot.say("User not found. Try learning how to type.")
        return
    
    username_dict[author] = username
    rewrite_username_file(username_dict)
    await bot.say("Username set. You should feel proud of yourself.")

@embed.error
async def embed_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.say("Wait {}m, {}s for the cooldown, you neanderthal.".format(int(error.retry_after / 60), int(error.retry_after) % 60))
    else:
        await bot.say("Unknown error occurred. You done fucked up big time.")

bot.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
