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
	await client.change_presence(game=discord.Game(name='n.help | nekobottm', type = 3))
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')

@client.event
async def on_message(message):
	if message.content.startswith('n.play '):
		author = message.author
		name = message.content.replace("n.play ", '')
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
	if message.content.startswith('n.help'):
		embed = discord.Embed(title="NEKOBOT™ 'S ANNOUNCEMENT", url="https://www.youtube.com/channel/UCSXSD0NwLC3eIT0yzPbkMFg", description="Nekobot masih dalam pembangunan dan masih di kembangkan", color=0x000000)
		embed.set_author(name="Nekobot™", url="https://www.youtube.com/channel/UCSXSD0NwLC3eIT0yzPbkMFg", icon_url="https://instagram.fcgk18-2.fna.fbcdn.net/vp/868f89f080937a0effabeb30e82f23f4/5CCAF5BE/t51.2885-19/s150x150/43054773_2180609508878724_2685255605483995136_n.jpg?_nc_ht=instagram.fcgk18-2.fna.fbcdn.net&_nc_cat=100")
		embed.add_field(name="Music command :", value="n.play | n.join | n.leave | n.pause | n.resume | n.stop", inline=True)
		await client.send_message(message.channel, embed=embed)
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
