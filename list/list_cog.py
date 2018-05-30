import discord
from discord.ext import commands
from list import list_data
from perms import perms_data
import time

class ListCog:
    def __init__(self, bot):
        self.bot = bot
        self.list_msgs = {}

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
                list_name = list_name[:-1]
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
                if index >= 0 and index < 5:
                    item = list_dict[index][0]
                    link = list_dict[index][1]
                description += str(index+1)+". ["+item+"]("+link+")\n"
            embed.description = description
            msg = await self.bot.say(embed=embed)

            self.list_msgs[msg.id] = (list_dict, 0)
            await self.bot.add_reaction(msg, '⬅')
            await self.bot.add_reaction(msg, '➡')

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
    async def additem(self, ctx, *args):
        try:
            index = int(args[0]) - 1
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
        
        list_data.add_to_list(current_list, index, item, link)
        await self.bot.say("List successfully updated.")

    @commands.command(pass_context=True)
    async def remitem(self, ctx, index):
        try:
            index = int(index) - 1
        except:
            index = -1

        try:
            current_list = list_data.get_current_list(ctx.message.author.id)
        except:
            await self.bot.say("You are not currently editing a list.")
            return

        list_data.remove_from_list(current_list, index)
        await self.bot.say("List successfully updated.")

    @commands.command(pass_context=True)
    async def addeditor(self, ctx, *args):
        if len(ctx.message.mentions) == 0:
            await self.bot.say("Please specify an editor.")
            return

        editor_id = ctx.message.mentions[0].id
        list_name = ""
        for arg in args[1:]:
            list_name += arg + "_"
        list_name = list_name[:-1]

        try:
            list_data.add_editor(ctx.message.author.id, list_name, editor_id)
            await self.bot.say(ctx.message.mentions[0].name+" can now edit your list.")
        except:
            await self.bot.say("That command failed.")

    @commands.command(pass_context=True)
    async def editlist(self, ctx, *args):
        if len(ctx.message.mentions) == 1:
            discord_id = ctx.message.mentions[0].id
            editor_id = ctx.message.author.id
            list_name = ""
            for arg in args[1:]:
                list_name += arg + "_"
            list_name = list_name[:-1]
        elif len(ctx.message.mentions) == 0:
            discord_id = ctx.message.author.id
            editor_id = ctx.message.author.id
            list_name = ""
            for arg in args:
                list_name += arg + "_"
            list_name = list_name[:-1]

        if editor_id not in list_data.get_editors(discord_id, list_name):
            await self.bot.say("You do not have permission to edit that list.")
            return
            
        try:
            list_data.switch_current_list(discord_id, list_name, editor_id)
            await self.bot.say("You are now editing list "+list_name.replace("_", " ")+".")
        except:
            await self.bot.say("That is not a list.")

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id not in self.list_msgs:
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.list_msgs:
            await self.flip_page(reaction, reaction.message, reaction.message.id)

    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id not in self.list_msgs:
            return
        elif user is reaction.message.author:
            return

        if reaction.message.id in self.list_msgs:
            await self.flip_page(reaction, reaction.message, reaction.message.id)

    async def flip_page(self, reaction, msg, msg_id):
        list_dict = self.list_msgs[msg_id][0]
        page = self.list_msgs[msg_id][1]

        if reaction.emoji == '➡':
            page += 1
            embed = discord.Embed(title=list_name.replace("_", " ")+", a list by "+ctx.message.author.name)
            for index in list_dict:
                if index >= page * 5 and index < (page + 1) * 5:
                    item = list_dict[index][0]
                    link = list_dict[index][1]
                description += str(index+1)+". ["+item+"]("+link+")\n"
            embed.description = description
            await self.bot.say(embed=embed)
            embed.set_footer(text="Page " + str(page+1))
        elif reaction.emoji == '⬅' and page > 0:
            page -= 1
            embed = discord.Embed(title=list_name.replace("_", " ")+", a list by "+ctx.message.author.name)
            for index in list_dict:
                if index >= page * 5 and index < (page + 1) * 5:
                    item = list_dict[index][0]
                    link = list_dict[index][1]
                description += str(index+1)+". ["+item+"]("+link+")\n"
            embed.description = description
            await self.bot.say(embed=embed)
            embed.set_footer(text="Page " + str(page+1))
        else:
            return

        self.list_msgs[msg_id] = (list_dict, page)
        await self.bot.edit_message(msg, embed=embed)

def setup(bot):
    bot.add_cog(ListCog(bot))
        
