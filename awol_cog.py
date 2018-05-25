import discord
from discord.ext import commands
from datetime import datetime, timedelta

class AWOLCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.server)
    async def awol(self, ctx):
        time = datetime.now() - timedelta(days=14)
        for member in self.bot.get_all_members():
            has_sent_message = False
            sorted_messages = sorted(self.bot.messages, key=lambda m: m.timestamp, reverse=True)
            most_recent_message = discord.utils.get(sorted_messages, author=member)
            if most_recent_message is None:
                pass
            elif most_recent_message.timestamp > time:
                has_sent_message = True
            if not has_sent_message:
                awol_role = discord.utils.get(self.bot.get_server('396053907543162881').role_hierarchy, id='449549299681067010')
                self.bot.add_roles(member, awol_role)


def setup(bot):
    bot.add_cog(AWOLCog(bot))
