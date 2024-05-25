import os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot("!", sync_commands_debug=True)


@bot.event
async def on_ready():
    print("The bot is ready")


@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong")


bot.run(TOKEN)
