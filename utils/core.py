from discord.ext import commands
import discord
import asyncio
import json

class core():

	def __init__(self, bot):

		self.bot = bot
		self.functions = {"help": self.help}

		self.errors = None
		self.build_vars()

	def build_vars(self):

		with open("utils/exceptions.json", "r") as er:

			self.errors = json.load(er)

	async def invoke(self, message, alias):

		if alias in self.functions:

			await self.functions[alias](message)

	async def help(self, message):

		preembed = discord.Embed(title="SFW Commands:", color=0xff00ff)
		preembed.add_field(name="!google <query>", value="returns relevant images from Google images", inline=True)

		embed = discord.Embed(title="NSFW Commands:", color=0xff00ff)
		embed.add_field(name="!hentai", value="finds random hentai from Gelbooru", inline=True)
		embed.add_field(name="!r34", value="works the same as hentai, but this time it gets images from rule34.xxx")
		embed.add_field(name="!hentai <tag>", value="finds hentai with the given tag - also works with !r34", inline=True)
		embed.add_field(name="!hentai <tag> <tag>", value="finds hentai with the given tags - also works with !r34", inline=True)

		await message.channel.send(embed=preembed)
		await message.channel.send(embed=embed)

	async def is_error(self, err):

		return str(err) in self.errors

	async def get_error(self, err):

		return self.errors[str(err)]