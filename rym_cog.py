import discord
from discord.ext import commands
import webcrawler
import rymdata

class RYMCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def rym(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
