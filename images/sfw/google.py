from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

from discord.ext import commands
import discord
import asyncio

class images():

	def __init__(self, bot, core):

		self.bot = bot
		self.core = core
		self.image_cache = {}
		self.message_cache = {}
		self.functions = {"google": self.google}

	async def invoke(self, message, alias):

		if alias in self.functions:

			await self.functions[alias](message)

	async def react(self, reaction, user):

		if user.id == 458100163429531648:

			return

		mid = reaction.message.id
		msgc = reaction.message.channel.id

		if msgc in self.message_cache:

			if self.message_cache[msgc]["mid"] == mid:

				if str(reaction.emoji) == u"\u27A1":

					delta = 1
					await self.build_update(msgc, delta)

				elif str(reaction.emoji) == u"\u2B05":

					delta = -1
					await self.build_update(msgc, delta)

	async def google(self, message):

		try:

			await self.is_tagged(message)
			await message.add_reaction("✅")
			await self.get_image(message)

		except Exception as err:

			await self.build_error(message, err)

	async def build_update(self, msgc, delta):

		index = self.message_cache[msgc]["index"]
		pos = index + delta

		if pos >= 0 and pos < 25:

			image = self.image_cache[msgc][pos]

			embed = discord.Embed(title=self.message_cache[msgc]["title"], color=0xff00ff)
			embed.set_image(url=image)

			self.message_cache[msgc]["index"] = index + delta
			await self.message_cache[msgc]["message"].edit(embed=embed)

	async def build_error(self, message, err):

		if await self.core.is_error(err):

			error = await self.core.get_error(err)
			await message.channel.send(error)

		else:

			await message.channel.send("Something went wrong! Here is the error...")
			await message.channel.send(str(err))

	async def is_tagged(self, message):

		if " " in message.content:

			tags = message.content.split(" ")
			del tags[0]

			if len(tags) < 1:

				await message.add_reaction("❌")
				raise Exception("query")

		else:

			await message.add_reaction("❌")
			raise Exception("query")

	async def get_image(self, message):

		tags = message.content.split(" ")
		del tags[0]

		url = "https://www.google.co.in/search?q="
		title = "results for '"
		for x in tags:

			url += x + "+"
			title += x + " "

		url = url[:len(url)-1] + "&source=lnms&tbm=isch"
		title = title[:len(title)-1] + "'"

		soup = await self.get_page(url)
		self.image_cache[message.channel.id] = await self.get_image_cache(soup)
		image = self.image_cache[message.channel.id][0]

		embed = discord.Embed(title=title, color=0xff00ff)
		embed.set_image(url=image)

		to_cache = await message.channel.send(embed=embed)
		cached_msg = {
			"message": to_cache,
			"title": title,
			"index": 0,
			"mid": to_cache.id
		}
		self.message_cache[message.channel.id] = cached_msg

		await to_cache.add_reaction(u"\u2B05")
		await to_cache.add_reaction(u"\u27A1")

	async def get_page(self, url):

		req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'})
		html = urlopen(req)
		soup = BeautifulSoup(html, "html.parser")

		return soup

	async def get_image_cache(self, soup):

		image_divs = soup.find_all("div", {"class": "rg_meta"})
		image_cache = []
		image_data = []

		index = 0
		for div in image_divs:

			image_data.append(json.loads(div.text))
			index += 1

			if index == 26:

				break

		for data in image_data:

			image_cache.append(data["ou"])

		return image_cache