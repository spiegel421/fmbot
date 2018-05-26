"""
The main program; when it runs, the bot runs. Commands are subdivided into
$fm and $rym, the first dealing with the last.fm API and the second with
the RateYourMusic scrapy webcrawler.

"""
import discord
from discord.ext import commands
import fm_cog, rym_cog, help_cog, awol_cog, perms_cog

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
fm_cog.setup(bot)
rym_cog.setup(bot)
help_cog.setup(bot)
awol_cog.setup(bot)
perms_cog.setup(bot)

with open('token.txt', 'r') as reader:
    bot.run(reader.read()[:-1])
