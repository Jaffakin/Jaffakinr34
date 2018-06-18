from discord.ext import commands
from main import main
import discord
import asyncio
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.INFO)
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
main = main(bot)

@bot.event
async def on_ready():

	print('Logged in as ' + str(bot.user.id))

	game=discord.Game(name="type !help for help")
	await bot.change_presence(game=game, status=discord.Status.online)

@bot.event
async def on_message(message):
	
	await main.process_message(message)

@bot.event
async def on_reaction_add(reaction, user):

	await main.process_reaction(reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):

	await main.process_reaction(reaction, user)

#place your bot's token between the quotes
bot.run("your token here")