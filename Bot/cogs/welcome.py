import discord
import random
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_messages = [
            "Welcome to the server! Hope you brought your A-game.",
            "A wild new member appeared! Welcome.",
            "Welcome to the dojo! Step inside and introduce yourself.",
            "Glad you could make it! Grab a seat and relax.",
            "Welcome to the grindhouse! Let's get to work.",
            "New player has joined the game. Welcome!",
            "Welcome! Mind your step and enjoy your stay.",
            "Ayo, welcome to the server! Great to have you here.",
            "You made it! Let the fun begin."
        ]
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel_id = 000000 # Make sure to replace this with your actual channel ID
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            message = random.choice(self.welcome_messages)
            await channel.send(f"{member.mention} {message}")



async def setup(bot):
    await bot.add_cog(Welcome(bot))