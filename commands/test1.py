import discord
from discord.ext import commands

class Test1Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="test1")
    async def test1(self, ctx):
        ctx.send("Test 1 Success.")
    
def setup(client):
    client.add_cog(Test1Commands(client))