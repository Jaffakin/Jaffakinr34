from images.nsfw.hentai import hentai
from images.sfw.google import images
from utils.core import core

from discord.ext import commands
import discord
import asyncio

class main():

	def __init__(self, bot):

		self.bot = bot
		self.core = core(bot)

		self.images = None
		self.hentai = None

		self.build_modules()

	def build_modules(self):

		self.images = images(self.bot, self.core)
		self.hentai = hentai(self.bot, self.core)

	async def process_message(self, message):

		if message.content.startswith("!"):

			await self.process_command(message)

	async def process_reaction(self, reaction, user):

		await self.images.process_reaction(reaction, user)

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
		await self.images.invoke(message, alias)
		await self.hentai.invoke(message, alias)