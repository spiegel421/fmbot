import discord
from discord.ext import commands
from random import randrange

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.id == '206277069678575616':
        r = randrange(0, 5) if '<@445843830860939265>' in message.content else randrange(0, 100)
        if r == 0:
            await client.send_message(message.channel, 'What the fuck did you just fucking say about me <@206277069678575616>, you little normie? I’ll have you know I graduated top of last weeks and this weeks contest, and I’ve been involved in receiving numerous prereleases, and I have over 300 confirmed album reviews. I am trained in genre recognition and I’m the top patrician in the entire Discord. You are nothing to me but just another normie. I will scrutinise and verbally assault the fuck out of any music you link with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of curators across the USA and your last.fm is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your "EDM". You’re fucking inauthentic, kid. I can hear music anywhere, anytime, and I can outmeme you in over seven hundred ways, and that’s just with my bare ears. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the RYM database and I will use it to its full extent to wipe your miserable ass off the face of the server, you little shit. If only you could have known what unholy retribution your little “clever” nightcore was about to bring down upon you, maybe you would have held off your fucking audacity. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking banned, kiddo.')

client.run('NDQ1ODQzODMwODYwOTM5MjY1.DdzE-g.kffUonxFS9M-0OMCUcwnAYErGYQ')
