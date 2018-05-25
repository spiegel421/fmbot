import discord
from discord.ext import commands
import awol_data

class AWOLCog:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        awol_data.add_timestamp(message.author.id, message.timestamp)
        await self.bot.process_commands(message)

    @commands.command(pass_context=True)
    async def awol(self, ctx):
        awol_users = awol_data.get_awol_users()
        print(len(awol_users))
        for user_id in awol_users:
            user = discord.utils.get(self.bot.get_all_members(), id=user_id)
            print(user.name)
            awol = discord.utils.get(user.server.roles, name="AWOL")

            await self.bot.add_roles(user, awol)

def setup(bot):
    bot.add_cog(AWOLCog(bot))
