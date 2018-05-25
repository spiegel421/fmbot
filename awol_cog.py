import discord
from discord.ext import commands
from datetime import datetime, timedelta

class AWOLCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
 #   @commands.cooldown(1, 86400, commands.BucketType.server)
    async def awol(self, ctx):
        time = datetime.now() - timedelta(days=14)
        members = []
        for member in self.bot.get_all_members():
            regular = discord.utils.get(member.server.roles, name="Regular")
            if regular in member.roles:
                members.append(member)
        print(len(members))
        count = 0
        for channel in self.bot.get_all_channels():
            count += 1
            try:
                async for message in self.bot.logs_from(channel, after=time):
                    if message.author in members:
                        members.remove(message.author)
                print(channel.name)
            except:
                print(channel.name + " INACCESSIBLE")

        print(count)
        print(len(members))
 #       for member in members:
#            awol = discord.utils.get(member.server.roles, name="AWOL")
#            await self.bot.add_roles(member, awol)


def setup(bot):
    bot.add_cog(AWOLCog(bot))
