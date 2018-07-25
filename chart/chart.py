import discord
from discord.ext import commands
from perms import perms_data

def ChartCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def chart(self, ctx):
        user_charts = chart_text = None
        if len(ctx.message.mentions) == 1:
            discord_id = ctx.message.mentions[0].id
            if len(args) == 1:
                user_charts = chart_data.get_user_charts(discord_id)
            else:
                chart_name = ""
                for arg in args[1:]:
                    chart_name += arg + "_"
                chart_name = chart_name[:-1]
                chart_text = chart_data.get_chart(discord_id, chart_name)
            elif len(ctx.message.mentions) == 0:
                discord_id = ctx.message.author.id
                if len(args) == 0:
                    user_charts = chart_data.get_user_charts(discord_id)
                else:
                    chart_name = ""
                    for arg in args:
                        chart_name += chart + "_"
                    chart_name = chart_name[:-1]
                    chart_text = chart_data.get_chart(discord_id, chart_name)

            description = ""
            if user_charts is not None:
                for user_chart in user_charts:
                    description += user_chart[0].replace("_", " ") + ", "
                description = description[:-1]
                await self.bot.say(description)
            if chart_text is not None:
                await self.bot.say(chart_text)

    @commands.command(pass_context=True)
    async def createchart(self, ctx, *args):
        chart_name = ""
        for arg in args:
            chart_name += arg + "_"
        chart_name = chart_name[:-3]
        chart_text = args[-1]

        try:
            chart_data.create_chart(ctx.message.author.id, chart_name, chart_text)
            await self.bot.say("Chart successfully created.")
        except:
            await self.bot.say("Chart creation failed.")

    @commands.command(pass_context=True)
    async def deletechart(self, ctx, *args):
        chart_name = ""
        for arg in args:
            chart_name += arg + "_"
        chart_name = chart_name[:-1]

        try:
            chart_data.delete_chart(ctx.message.author.id, chart_name)
            await self.bot.say("Chart successfully deleted.")
        except:
            await self.bot.say("Chart deletion failed.")

    @commands.command(pass_context=True)
    async def editchart(self, ctx, *args):
        discord_id = ctx.message.author.id

        chart_name = ""
        for arg in args:
            chart_name += arg + "_"
        chart_name = chart_name[:-1]

        try:
            chart_data.switch_current_list(discord_id, chart_name)
            await self.bot.say("You are now editing chart "+chart_name.replace("_"," ")+".")
        except:
            await self.bot.say("That is not a chart.")

def setup(bot):
    bot.add_cog(ChartCog(bot))
