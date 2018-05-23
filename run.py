"""
The main program; when it runs, the bot runs. Commands are subdivided into
$fm and $rym, the first dealing with the last.fm API and the second with
the RateYourMusic scrapy webcrawler.

"""
import discord
from discord.ext import commands
import fm_cog, rym_cog

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
fm_cog.setup(bot)
rym_cog.setup(bot)

@bot.event
async def on_message(message):
    if message.content.lower().startswith('&help'):
        commands={}
        commands['&fm'] = 'Displays your most recently scrobbled track'
        commands['&fm set <username>'] = 'Sets your lastfm username'
        commands['&fm topartists'] = 'Displays your top artists on lastfm'
        commands['&fm trendingartists <num_days>'] = 'Displays the most scrobbled artists on the server within the past num_days'
        commands['&rym'] = 'Gives the link to your RYM account'
        commands['&rym set <RYM username>'] = 'Sets the link to your RYM account'
        commands['&rym get <Discord username>'] = 'Finds the RYM account of another user'
        
        embed = discord.Embed(title='Sean', description="Written by Justin S",color=0x0000ff)
        for command,description in commands.items():
            embed.add_field(name=command, value=description, inline=False)
        await bot.say(embed=embed)

    await bot.process_commands(message)

with open('token.txt', 'r') as reader:
    bot.run(reader.read()[:-1])
