from images.nsfw.modules.hentai import hentai
from images.nsfw.modules.r34 import r34

from discord.ext import commands
import discord
import asyncio

class lewd():

	def __init__(self, bot, core):

		self.r34 = r34(bot, core)
		self.hentai = hentai(bot, core)

		self.functions = None
		self.build_functions()

	def build_functions(self):

		self.functions = {
			"r34": self.r34.exec_function,
			"hentai": self.hentai.exec_function
		}

	async def invoke(self, message, alias):

		if alias in self.functions:

			await self.functions[alias](message)

	async def react(self, reaction, user):

		mid = reaction.message.id
		msgc = reaction.message.channel.id
		delta = await self.delta(reaction)
		if delta == 0:

			return

		rcache =  await self.r34.get_cache()
		hcache = await self.hentai.get_cache()

		if msgc in rcache:
			if rcache[msgc]["mid"] == mid:

				await self.r34.build_update(msgc, delta)

		if msgc in hcache:
			if hcache[msgc]["mid"] == mid:	

				await self.hentai.build_update(msgc, delta)

	async def delta(self, reaction):

		if str(reaction.emoji) == u"\u27A1":

			return 1

		if str(reaction.emoji) == u"\u2B05":

			return -1

		return 0
