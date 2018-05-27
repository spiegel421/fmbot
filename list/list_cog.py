import discord
from discord.ext import commands
from list import list_data
from perms import perms_data
import time

class ListCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def list(self, ctx, *, args):
        user_lists = list_dict = None
        if len(ctx.message.mentions) == 1:
            discord_id = ctx.message.mentions[0].id
            if len(args) == 1:
                user_lists = list_data.get_user_lists(discord_id)
            else:
                list_dict = list_data.get_list(discord_id, args)
        elif len(ctx.message.mentions) == 0:
            discord_id = ctx.message.author.id
            if len(args) == 0:
                user_lists = list_data.get_user_lists(discord_id)
            else:
                list_dict = list_data.get_list(discord_id, args)

        description = ""
        if user_lists is not None:
            for user_list in user_lists:
                description += user_list + "\n"
            description = description[:-1]
        embed = discord.Embed(description=description)
        if list_dict is not None:
            for index in list_dict:
                item = list_dict[index][0]
                link = list_dict[index][1]
                desc = list_dict[index][2]
                embed.add_field(name=index+". ["+item+"]("+link+")", value=desc)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def createlist(self, ctx, *, args):
        list_data.create_list(ctx.message.author.id, args)
        await bot.say("List successfully created.")

def setup(bot):
    bot.add_cog(ListCog(bot))
        
