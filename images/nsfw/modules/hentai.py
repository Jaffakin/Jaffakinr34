from urllib.request import Request, urlopen
from random import randint as rand
from discord.ext import commands
from bs4 import BeautifulSoup
import discord
import asyncio

class hentai():

	def __init__(self, bot, core):

		self.bot = bot
		self.core = core
		self.image_cache = {}
		self.message_cache = {}

		self.base_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100"

	async def exec_function(self, message):

		try:

			await self.is_nsfw(message)
			await self.get_hentai(message)

		except Exception as err:

			await self.build_error(message, err)

	async def build_update(self, msgc, delta):

		index = self.message_cache[msgc]["index"]
		pos = index + delta
		if pos >= 0 and pos < len(self.image_cache[msgc]):

			image = self.image_cache[msgc][pos][0]
			title_url = self.image_cache[msgc][pos][1]
			embed = discord.Embed(title="click me for sauce", url=title_url, color=0xff00ff)
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

	async def get_hentai(self, message):

		url = await self.get_url(message)
		soup = await self.get_page(url)

		self.image_cache[message.channel.id] = await self.get_image_cache(soup)
		image = self.image_cache[message.channel.id][0][0]
		title_url = self.image_cache[message.channel.id][0][1]
		embed = discord.Embed(title="click me for sauce", url=title_url, color=0xff00ff)
		embed.set_image(url=image)

		to_cache = await message.channel.send(embed=embed)
		cached_msg = {"message": to_cache,"index": 0,"mid": to_cache.id}
		self.message_cache[message.channel.id] = cached_msg

		await to_cache.add_reaction(u"\u2B05")
		await to_cache.add_reaction(u"\u27A1")

	async def get_page(self, url):

		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		html = urlopen(req).read()
		soup = BeautifulSoup(html,"lxml")

		return soup

	async def get_image_cache(self, soup):

		targets = soup.find_all("post")
		image_cache = []
		for img in targets:

			src = img["file_url"]
			src = "https://gelbooru.com/" + src[27:]

			sauce = img["id"]
			sauce = "https://gelbooru.com/index.php?page=post&s=view&id=" + str(sauce)

			image_cache.append((src, sauce))

		return image_cache

	async def get_url(self, message):

		try:

			tags = message.content.split(" ")
			del tags[0]

			url = self.base_url + "&tags=rating%%3Aexplicit+"
			if len(tags) > 0:
				for x in tags:

					url += x + "+"

			soup = await self.get_page(url)
			pid = int(soup.find("posts")["count"])
			if pid < 1:

				raise Exception

			pid = pid // 100
			if pid > 200:

				pid = 200

			url += "&pid=" + str(rand(0, pid))
			return url

		except:

			raise Exception("null")

	async def get_cache(self):

		return self.message_cache

	async def is_nsfw(self, message):

		if not message.channel.is_nsfw():

			await message.add_reaction("❌")
			raise Exception("nsfw")

		else:

			await message.add_reaction("✅")