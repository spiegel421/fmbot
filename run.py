"""
The main program; when it runs, the bot runs. Commands are subdivided into
$fm and $rym, the first dealing with the last.fm API and the second with
the RateYourMusic scrapy webcrawler.

"""
import discord
from discord.ext import commands
import fm_cog, rym_cog, help_cog

bot = commands.Bot(command_prefix='$')
fm_cog.setup(bot)
rym_cog.setup(bot)
help_cog.setup(bot)

@bot.command()
async def genres(artist, album):
    genrecrawl.edit_genre_file(artist, album)
    
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

@genres.error
async def genre_error(error, ctx):
    await bot.say("Artist or album not found. Uh, make sure you're searching for music, I guess.")

with open('token.txt', 'r') as reader:
    bot.run(reader.read()[:-1])
