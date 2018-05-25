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
            messages = discord.utils.get(self.bot.messages, author=member)
            try:
                for message in messages:
                    if message.timestamp < time:
                        break
                    elif member == message.author:
                        has_sent_message = True
                        break
                if not has_sent_message:
                    awol_role = discord.utils.get(self.bot.get_server('243129311421399050').role_hierarchy, id='449549299681067010')
                    self.bot.add_roles(member, awol_role)
            except:
                continue

def setup(bot):
    bot.add_cog(AWOLCog(bot))
