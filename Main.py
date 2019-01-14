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
client.remove_command("help")

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
    
    if message.content.startswith('xplay '):
	author = message.author
	name = message.content.replace("xplay ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	delmsg = await client.send_message(message.channel, 'Now Playing ** >> ' + title + '**')
	server = message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url)
	players[server.id] = player
	print("User: {} From Server: {} is playing {}".format(author, server, title))
	player.start()
     await client.process_commands(message)

@client.command(pass_context=True, no_pm=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('Connected to voice channel: **[' + str(channel) + ']**')

@client.command(pass_context=True, no_pm=True)
async def leave(ctx):
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say("Successfully disconnected from ***[{}]***".format(channel))

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say("Player Paused")

@client.command(pass_context=True)
async def stop(ctx):
    author = ctx.message.author
    id = ctx.message.server.id
    players[id].stop()
    await client.say("Player Stopped")

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say("player resumed")
    
client.run(os.environ['BOT_TOKEN'])
