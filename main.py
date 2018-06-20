from images.sfw.google import images
from images.nsfw.lewd import lewd
from utils.core import core

from discord.ext import commands
import discord
import asyncio

class main():

	def __init__(self, bot):

		self.bot = bot
		self.core = core(bot)

		self.lewd = None
		self.images = None

		self.build_modules()

	def build_modules(self):

		self.lewd = lewd(self.bot, self.core)
		self.images = images(self.bot, self.core)

	async def process_author(self, author:int):

		if author == self.bot.user.id:

			return False

		return True

	async def process_message(self, message):

		if message.content.startswith("!"):

			if await self.process_author(message.author.id):

				await self.process_command(message)

	async def process_reaction(self, reaction, user):

		if await self.process_author(user.id):

			await self.lewd.react(reaction, user)
			await self.images.react(reaction, user)

	async def process_command(self, message):

		content = message.content
		alias = await self.parse_command(content)

		await self.exec_command(message, alias)

	async def parse_command(self, content):

		if " " in content:

			return content[1:content.find(" ")]

		return content[1:]

	async def exec_command(self, message, alias):

		await self.core.invoke(message, alias)
		await self.lewd.invoke(message, alias)
		await self.images.invoke(message, alias)