import discord
import requests
import json
from discord.ext import commands

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_meme(self):
        response = requests.get('https://meme-api.com/gimme')
        json_data = json.loads(response.text)
        return json_data['url']

    @commands.command()
    async def meme(self, ctx):
        meme_url = self.get_meme()
        await ctx.send(meme_url)


async def setup(bot):
    await bot.add_cog(Meme(bot))
