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

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('friend'):
    f1hash = message.content.find('#')
    f1username = message.content[7:f1hash]
    f1userdisc = message.content[f1hash + 1:]
    for j in client.get_all_members():
      if (j.name == f1username and j.discriminator == f1userdisc):
        member = await client.fetch_user(j.id)
        await member.send(message.author.name + " wants to check in with you!")

client.run(os.getenv('TOKEN'))