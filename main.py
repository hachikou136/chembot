import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', case_insensitive = True, intents = intents)

@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Game(name="with chemicals"))
    print("We have logged in as", bot.user)
    await load_extensions()

EXTENSIONS = [
    'cogs.element',
    'cogs.compound',
    'cogs.galvanic_cell',
    # 'cogs.quiz' # disable loading this extension, because this extension raise an unknown error.
]

async def load_extensions():
  for extension in EXTENSIONS:
      await bot.load_extension(extension)

keep_alive()

token = os.environ['TOKEN']

bot.run(token)