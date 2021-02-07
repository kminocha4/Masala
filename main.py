import discord
import os
import requests
import json

from dotenv import load_dotenv
from discord.ext import commands,tasks
from itertools import cycle
load_dotenv()

intents = discord.Intents.default()
intents.members = True 
client=commands.Bot(command_prefix='.',intents=intents)
#client = discord.Bot(prefix = '.', intents=intents)

status=cycle(['Status 1','Status 2'])

  
@client.event
async def on_ready():
  change_status.start()
  print('BOT IS READY')

@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

@client.command()
async def check_In(ctx):
  print(ctx.message.author)
  
  await ctx.author.send('Checking In!')
 
@client.command()
async def dm(ctx,user: discord.User,*,args=None):
  await user.send("hi")


@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
  
  for i in client.get_all_channels():
    print(i)
    if(i.name=="general"):
      channel=client.get_channel(i.id)
      await channel.send("30 second message")
  
  for j in client.get_all_members():
    if j.name=="fisha":
      break
    
  #channel = client.get_channel(os.getenv('GUILD_ID'))
  #channel.send("Message")

client.run(os.getenv("TOKEN"))
#client.run(os.getenv('TOKEN'))