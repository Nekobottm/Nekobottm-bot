import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import requests, bs4
import os
import random
import youtube_dl
from discord import opus

client = commands.Bot(command_prefix = 'n.')

players = {}

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name='n.help | youtube.com/nekobot'))
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')

@client.event
async def on_message(message):
    if message.content.startswith('n.help'):
        embed = discord.Embed(title="Nekobot™'s Announcement", description="Bot masih dalam pembangunan dan belum terdapat command pada bot", color=0x00ff00)
        embed.add_field(name="Command List :", value="n.help", inline=False)
        embed.add_field(name="Update", value="- penambahan music play", inline=False)
        await client.send_message(message.channel, embed=embed)
    if message.content == 'n.ping':
        await client.send_message(message.channel,'pong')
    await client.process_commands(message)
    
client.run(os.environ['BOT_TOKEN'])
