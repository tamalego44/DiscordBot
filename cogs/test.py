import discord
from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="test1")
    async def test1(self, ctx):
        await ctx.send("Test 1 Success.")
    
async def setup(client):
    await client.add_cog(TestCommands(client))