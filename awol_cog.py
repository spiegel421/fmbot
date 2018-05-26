import discord
from discord.ext import commands
import awol_data

class AWOLCog:
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(ctx):
        return ctx.author.id == '359613794843885569'

    async def on_message(self, message):
        regular = discord.utils.get(message.server.roles, name='Regular')
 #       if regular in message.author.roles:
        awol_data.add_timestamp(message.author.id, message.timestamp)
        await self.bot.process_commands(message)

    @commands.group(pass_context=True)
    async def awol(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        
        awol_users = awol_data.get_awol_users()
        for member_id in awol_users:
            member = discord.utils.get(self.bot.get_all_members(), id=member_id)
            awol = discord.utils.get(member.server.roles, name="AWOL")
            await self.bot.add_roles(member, awol)

    @awol.command(pass_context=True)
    @commands.check(is_owner)
    async def start(self, ctx):
        for member in self.bot.get_all_members():
 #           regular = discord.utils.get(ctx.message.server.roles, name='Regular')
 #           if regular in ctx.message.author.roles:
            await self.bot.add_roles(member, role)

def setup(bot):
    bot.add_cog(AWOLCog(bot))
