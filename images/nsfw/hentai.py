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
		self.functions = {
			"r34": self.r34,
			"hentai": self.hentai
		}

	async def invoke(self, message, alias):

		if alias in self.functions:

			await self.functions[alias](message)

	async def hentai(self, message):

		try:

			await self.is_nsfw(message)

			if await self.is_tagged(message):

				await self.get_tagged_hentai(message)

			else:

				await self.get_hentai(message)

		except Exception as err:

			await self.build_error(message, err)

	async def r34(self, message):

		try:

			await self.is_nsfw(message)

			if await self.is_tagged(message):

				await self.get_tagged_r34(message)

			else:

				await self.get_r34(message)

		except Exception as err:

			await self.build_error(message, err)

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

			if len(tags) >= 1:

				return True

		return False

	async def is_nsfw(self, message):

		if not message.channel.is_nsfw():

			await message.add_reaction("❌")
			raise Exception("nsfw")

		else:

			await message.add_reaction("✅")

	async def is_null(self, target):

		if len(target) == 0:

			raise Exception("null")

	async def get_hentai(self, message):

		#gelbooru only lets you go so far back, and 500 was past this limit so I just went with 420
		#times 42 because there are 42 images per page, and this is how gelbooru handles page id
		page_id = str(rand(0,420) * 42)
		url = "https://gelbooru.com/index.php?page=post&s=list&tags=rating%%3aexplicit+&pid=" + page_id

		soup = await self.get_page(url)
		embed = await self.get_image(soup, "hentai")

		await message.channel.send(embed=embed)

	async def get_tagged_hentai(self, message):

		tags = message.content.split(" ")
		del tags[0]

		url = "https://gelbooru.com/index.php?page=post&s=list&tags=rating%%3aexplicit+"

		for x in tags:

			url += x + "+"

		soup = await self.get_page(url)
		source = soup.prettify()
		max_pages = 0

		if "pid=" in source:

			source = source[source.rfind("pid="):]
			source = source[source.find('=')+1:source.find('"')]

			max_pages = int(source)

		if max_pages > 17640:

			max_pages = 17640

		url += "&pid=" + str(max_pages)

		soup = await self.get_page(url)
		embed = await self.get_image(soup, "hentai")

		await message.channel.send(embed=embed)

	async def get_r34(self, message):

		#gelbooru only lets you go so far back, and 500 was past this limit so I just went with 420
		#times 42 because there are 42 images per page, and this is how gelbooru handles page id
		#yes, the r34 site is running on gelbooru as well
		page_id = str(rand(0,420) * 42)
		url = "https://rule34.xxx/index.php?page=post&s=list&tags=rating%3Aexplicit&pid=" + page_id

		soup = await self.get_page(url)
		embed = await self.get_image(soup, "r34")

		await message.channel.send(embed=embed)

	async def get_tagged_r34(self, message):

		tags = message.content.split(" ")
		del tags[0]

		url = "https://rule34.xxx/index.php?page=post&s=list&tags=rating%%3aexplicit+"

		for x in tags:

			url += x + "+"

		soup = await self.get_page(url)
		source = soup.prettify()
		max_pages = 0

		if "pid=" in source:

			source = source[source.rfind("pid="):]
			source = source[source.find('=')+1:source.find('"')]

			max_pages = int(source)

		if max_pages > 17640:

			max_pages = 17640

		url += "&pid=" + str(max_pages)

		soup = await self.get_page(url)
		embed = await self.get_image(soup, "r34")

		await message.channel.send(embed=embed)

	async def get_page(self, url):

		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		html = urlopen(req).read()
		soup = BeautifulSoup(html,"html.parser")

		return soup

	async def get_image(self, soup, cmd:str):

		if cmd == "r34":

			target = soup.find_all("img", class_="preview")
			await self.is_null(target)

			target = target[rand(0,len(target)-1)]["src"]
			image_id = target[target.rfind("?")+1:]

			url = "https://rule34.xxx/index.php?page=post&s=view&id=" + image_id
			soup = await self.get_page(url)
			image = soup.find("img", id="image")["src"]
			image = "https://rule34.xxx/" + image[image.find("xxx") + 5:]

		else:

			target = soup.find_all("img", class_="preview ")
			await self.is_null(target)

			target = target[rand(0,len(target)-1)]["alt"]
			image_id = target.split(" ")[1]

			url = "https://gelbooru.com/index.php?page=post&s=view&id=" + image_id
			soup = await self.get_page(url)
			image = soup.find("img")["src"]
			image = "https://gelbooru.com/" + image[28:]

		embed = discord.Embed(title="click me for sauce", url=str(url), color=0xff00ff)
		embed.set_image(url=image)
		return embed