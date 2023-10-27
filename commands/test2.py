import discord
from discord.ext import commands

class Test2Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="test2")
    async def test1(self, ctx):
        ctx.send("Test 2 Success.")
    
def setup(client):
    client.add_cog(Test2Commands(client))