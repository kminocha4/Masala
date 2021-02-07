import discord
import os
import requests
import json

from dotenv import load_dotenv
from discord.ext import commands,tasks
from itertools import cycle
from datetime import datetime
import random

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
  check_dead_channel.start()
  send_check_ins.start()
  print('BOT IS READY')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server! I am Masala Bot :robot:, here to spice up your conversations :hot_pepper:. To get started, help me understand more about you :cowboy:. What are your interests? :art: :performing_arts: :woman_scientist: :french_bread: :musical_note: Let me start! I love spicy food :hot_pepper: :yum: and ballroom dancing :dancer:! Head on over to the roles channel on the server and add your interests!'
    )

@tasks.loop(seconds=30)
async def check_dead_channel():
 
  for i in client.get_all_channels():
    print(i)
    if(i.name=="general"):
      #channel=client.get_channel(i.id)
      #await channel.send("30 second check-in! :eyes:")
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
  

@tasks.loop(seconds=60)
async def send_check_ins():
  check_ins=["What is something you are doing today to practice self-care? :love_you_gesture: ","If you are feeling stressed out, try some yoga! :blush:","Go outside, touch some grass. :evergreen_tree:", "Get up and dance for two minutes! :dancer:", "Listen to some good music and share them with some people around you!:musical_note: ", "Reach out to someone! :hugging: (Helpful tip: if you type 'friend name#discriminatorNumber' then I'll send them a check-in from you!) :smile:"]
  for j in client.get_all_members():
    print(j)
    if(j.name!="masala dosA" and j.name!="testbot" and j.name!="masala"):
      member=await client.fetch_user(j.id)
      await member.send("Hi there! It's your friend Masala Bot :robot: :hot_pepper: here for your check-in! :innocent: \nFeel free to reflect on those feelings! :grinning: :cry: :rage: :worried: :sunglasses: \nI'll always be here for you :heart:")
      response = "My tip/question: "+ random.choice(check_ins)
      await member.send(response)

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