import discord
from discord.ext import commands
import time
from dotenv import load_dotenv
from os import getenv
import os
from rich import print

load_dotenv(".env")

TOKEN = getenv("TOKEN")
PREFIX = "]"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX,
                      case_insensitive=True, intents=intents)


@commands.command()
@client.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.event
async def on_ready():
    print(f"[green bold][{time.strftime('%T')}] Logged in as {client.user}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.competing, name=f"a future Codejam!"
        )
    )


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument.")


client.run(TOKEN)
