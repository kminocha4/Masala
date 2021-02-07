import discord
import os
import requests
import json
import random
from datetime import datetime

from dotenv import load_dotenv
from discord.ext import commands,tasks
from itertools import cycle
load_dotenv()

icebreakers = [
  "Is lasagna a sandwich? Discuss.",
  "What are your favorite childhood TV shows?",
  "If you could visit any fictional world, where would you go?",
  "If you were a vending machine, what would you vend?",
  "Post your funniest memes. Go!",
  "Tell your best dad joke.",
  "If you could have any question answered, what would it be?",
  "If you could have dinner with anyone - dead or alive - who would you choose?",
  "Let's play two truths and a lie! I'll start: 1. I can feel emotions. 2. I am 2 days old. 3. My favorite color is blurple.",
  "What would the book/movie of your life story be like? What would it be called?",
  "Toilet paper roll: facing in or out? Discuss.",
  "What is your favorite guilty pleasure TV show?",
  "Tell us about your socks. What is your favorite type of socks? Favorite pair?",
]

intents = discord.Intents.default()
intents.members = True 
client=commands.Bot(command_prefix='.',intents=intents)
#client = discord.Bot(prefix = '.', intents=intents)

status=cycle(['Status 1','Status 2'])

def get_icebreaker():
  quote = random.choice(icebreakers)
  return(quote)

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
    if(i.type == discord.ChannelType.text):
      channel=client.get_channel(i.id)
      #maya_testing = client.get_channel(807817639559823421)
      #await channel.send("30 second check-in!")
      msg = await channel.history(limit=1).flatten()
      timestamp = msg[0].created_at
      current_time = datetime.now()
      difference = current_time - timestamp
      diff_s = difference.total_seconds()
      if msg[0].author == client.user:
       return
      if (diff_s > 120):
        await channel.send('This channel is pretty dead, huh? ' + get_icebreaker())


client.run('ODA3NzA0NzAwMzU4NzU0MzQ0.YB73ng.Gl6ssQ31i4eMhGViiL9GPpV9G8c')