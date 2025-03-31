import discord
from discord.ext import commands

class Gambling(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="ccreate")
    async def test2(self, ctx):
        await ctx.send("Test 1 Success.")

        print(ctx.__dict__())
    
async def setup(client):
    await client.add_cog(Gambling(client))



"""
Card create:
    Creates a new card for people to gamble on
    - title: What are people betting on
    - options: 2+ diff named options
    
Habiba

    
"""