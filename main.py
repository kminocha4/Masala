import discord
import os
import requests
import json
from datetime import datetime

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
 



@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))
  for i in client.get_all_channels():
    print(i)
    if(i.name=="general"):
      #channel=client.get_channel(i.id)
      maya_testing = client.get_channel(807812132003512320)
      #await channel.send("30 second check-in!")
      msg = await maya_testing.history(limit=1).flatten()
      timestamp = msg[0].created_at
      current_time = datetime.now()
      difference = current_time - timestamp
      diff_s = difference.total_seconds()
      if msg[0].author == client.user:
        return
      if (diff_s > 120):
        await maya_testing.send('This channel is pretty dead, huh?')
  for j in client.get_all_members():
    if j.name=="fisha":
      member=await client.fetch_user(j.id)
      await member.send("60 second check-in")
  #except:
    #print("You probably need a new token!")

client.run('ODA3NzA0NzAwMzU4NzU0MzQ0.YB73ng.QxZGNYZvLXgOMiiqRt-aVSJiQJY')