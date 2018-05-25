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
            if member.roles.has('449652864256835627'):
                members.append(member)
        for channel in self.bot.get_all_channels():
            async for message in self.bot.logs_from(channel, after=time):
                if message.author in members:
                    members.remove(message.author)
        print(len(members))
        for member in members:
            role = discord.utils.get(member.server.roles, name="AWOL")
            await self.bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(AWOLCog(bot))
