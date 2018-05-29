import discord
from discord.ext import commands
from list import list_data
from perms import perms_data
import time

class ListCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def list(self, ctx, *args):
        user_lists = list_dict = None
        if len(ctx.message.mentions) == 1:
            discord_id = ctx.message.mentions[0].id
            if len(args) == 1:
                user_lists = list_data.get_user_lists(discord_id)
            else:
                list_name = ""
                for arg in args[1:]:
                    list_name += arg + "_"
                list_name = list_name[:-1].r
                list_dict = list_data.get_list(discord_id, list_name)
        elif len(ctx.message.mentions) == 0:
            discord_id = ctx.message.author.id
            if len(args) == 0:
                user_lists = list_data.get_user_lists(discord_id)
            else:
                list_name = ""
                for arg in args:
                    list_name += arg + "_"
                list_name = list_name[:-1]
                list_dict = list_data.get_list(discord_id, list_name)

        description = ""
        if user_lists is not None:
            for user_list in user_lists:
                description += user_list[0] + " "
            description = description[:-1]
            await self.bot.say(description)
        if list_dict is not None:
            embed = discord.Embed(title=list_name.replace("_", " ")+", a list by "+ctx.message.author.name)
            for index in list_dict:
                item = list_dict[index][0]
                link = list_dict[index][1]
                description += str(index+1)+". ["+item+"]("+link+")"
            embed.description = description
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def createlist(self, ctx, *args):
        list_name = ""
        for arg in args:
            list_name += arg + "_"
        list_name = list_name[:-1]

        try:
            list_data.create_list(ctx.message.author.id, list_name)
            await self.bot.say("List successfully created.")
        except:
            await self.bot.say("List creation failed.")

    @commands.command(pass_context=True)
    async def deletelist(self, ctx, *args):
        list_name = ""
        for arg in args:
            list_name += arg + "_"
        list_name = list_name[:-1]

        try:
            list_data.delete_list(ctx.message.author.id, list_name)
            await self.bot.say("List successfully deleted.")
        except:
            await self.bot.say("List deletion failed.")

    @commands.command(pass_context=True)
    async def add(self, ctx, *args):
        index = None
        try:
            index = int(args[0])
        except:
            index = -1

        try:
            if index == -1:
                link = args[0]
                item = ' '.join(args[1:])
            else:
                link = args[1]
                item = ' '.join(args[2:])
        except:
            await self.bot.say("Please specify both an item and a link.")
            return

        try:
            current_list = list_data.get_current_list(ctx.message.author.id)
        except:
            await self.bot.say("You are not currently editing a list.")
            return
        
        list_data.add_to_list(ctx.message.author.id, current_list, index, item, link)
        await self.bot.say("List successfully updated.")

    @commands.command(pass_context=True)
    async def edit(self, ctx, list_name):
        try:
            list_data.switch_current_list(ctx.message.author.id, list_name)
            await self.bot.say("You are now editing list "+list_name+".")
        except:
            await self.bot.say("That is not a list.")

def setup(bot):
    bot.add_cog(ListCog(bot))
        
