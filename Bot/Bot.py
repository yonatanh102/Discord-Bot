import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

simple_role = "Peasant"

async def load_extensions():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
      await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
  print(f"We are ready to go in, {bot.user.name}")
  try:
    synced = await bot.tree.sync()
    print(f"🔁 Synced {len(synced)} slash commands.")
  except Exception as e:
    print(f"❌ Failed to sync commands: {e}")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  await bot.process_commands(message)

@bot.command()
async def hello(ctx):
  await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def help(ctx):
  await ctx.send("Use '?' or '/' before any of the mentioned commands \n "
                 "1) Music commands: \n"
                 "/play - ""name/url"" plays the mentioned song\n"
                 "/skip - skips one song in the queue\n"
                 "/pause - pauses the current song\n"
                 "/resume - resumes the current song\n"
                 "/leave - stop the song, clears the queue and leaving the VC\n"
                 "2) diffrent utility commands\n"
                 "?dm ""msg"" - sends the msg through the bot to the person mentioned\n "
                 "?poll ""msg"" - creates a poll with 'yes' or 'no comments")

@bot.command()
async def assign(ctx):
  role = discord.utils.get(ctx.guild.roles, name=simple_role)
  if role:
    await ctx.author.add_roles(role)
    await ctx.send(f"{ctx.author.mention} is now a {simple_role}")
  else:
    await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
  role = discord.utils.get(ctx.guild.roles, name=simple_role)
  if role:
    await ctx.author.remove_roles(role)
    await ctx.send(f"{ctx.author.mention} is no longer a {simple_role}")
  else:
    await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
  await ctx.author.send(f"{msg}")

@bot.command()
async def poll(ctx, *, question):
  embed = discord.Embed(title="New Poll", description=question)
  poll_message = await ctx.send(embed=embed)
  await poll_message.add_reaction("👍")
  await poll_message.add_reaction("👎")

async def main():
    await load_extensions()
    await bot.start(token)

asyncio.run(main())
