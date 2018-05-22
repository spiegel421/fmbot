import discord
from discord.ext import commands
from random import randrange

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.id == '206277069678575616':
        r = randrange(0, 100)
        if r == 0:
            await client.send_message(message.channel, 'Shut the fuck up, <@206277069678575616>.')

client.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
