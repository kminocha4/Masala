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
  try:
    for i in client.get_all_channels():
      print(i)
      if(i.name=="general"):
        channel=client.get_channel(i.id)
        await channel.send("30 second check-in! :eyes:")
    for j in client.get_all_members():
      if j.name=="fisha":
        member=await client.fetch_user(j.id)
        await member.send("60 second check-in")
  except:
    print("You probably need a new token!")


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