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
            members.append(member)
        for channel in self.bot.get_all_channels():
            async for message in self.bot.logs_from(channel, after=time):
                if message.author in members:
                    members.remove(message.author)
        for member in members:
            self.bot.add_role(member, '449558462154801162')


def setup(bot):
    bot.add_cog(AWOLCog(bot))
