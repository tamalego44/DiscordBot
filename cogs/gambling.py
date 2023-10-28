import discord
from discord.ext import commands

class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="test2")
    async def test2(self, ctx):
        await ctx.send("Test 1 Success.")
    
async def setup(client):
    await client.add_cog(Gambling(client))