
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

icebreakers = [
  "Is lasagna a sandwich?:sandwich:",
  "What are your favorite childhood TV shows?:tv: ",
  "If you could visit any fictional world, where would you go? :map: ",
  "If you were a vending machine, what would you vend? :beverage_box: ",
  "Post your funniest memes. :yum:  Go!",
  "Tell your best dad joke. :laughing: ",
  "If you could have any question answered, what would it be:question: ",
  "If you could have dinner with anyone - dead or alive - who would you choose? I don't count! :rofl: ",
  "Let's play two truths and a lie! :stuck_out_tongue_closed_eyes:  I'll start: 1. I can feel emotions. 2. I am 2 days old. 3. My favorite color is blurple.",
  "What would the book/movie :book:  of your life story be like? What would it be called? :thinking: ",
  "Toilet paper roll: facing in or out? :roll_of_paper: Discuss.",
  "What is your favorite guilty pleasure TV show? :yum: ",
  "Tell us about your socks. What is your favorite type of socks? Favorite pair? :socks: ",
]

intents = discord.Intents.default()
intents.members = True 
client=commands.Bot(command_prefix='.',intents=intents)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


def get_icebreaker():
  quote = random.choice(icebreakers)
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
        await channel.send('This channel is pretty dead, huh? \n' + get_icebreaker())

  

@tasks.loop(seconds=60)
async def send_check_ins():
  check_ins=["What is something you are doing today to practice self-care? :smiling_face_with_3_hearts: ","If you are feeling stressed out, try some yoga! :love_you_gesture: ","Go outside, touch some grass. :evergreen_tree:", "Get up and dance for two minutes! :dancer:", "Listen to some good music and share them with some people around you!:musical_note: ", "Reach out to someone! :hugging: (Helpful tip: if you type 'friend name#discriminatorNumber' then I'll send them a check-in from you!) :smile:"]
  for j in client.get_all_members():
   # print(j)
    if(j.name!="masala dosA" and j.name!="testbot" and j.name!="masala"):
      member=await client.fetch_user(j.id)
      await member.send("Hi there! It's your friend Masala Bot :robot: :hot_pepper: here for your check-in! :innocent: \nPost an emoji in our chat like so: .feeling <emoji>\nFeel free to reflect on those feelings! :grinning: :cry: :rage: :worried: :sunglasses:")
      response = "My tip/question: "+ random.choice(check_ins)
      await member.send(response)

@client.event
async def on_message(message):
  if message.author == client.user:
    return


  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)


arr={}
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
        await member.send("Hi "+j.name+ ", your friend, "+message.author.name + " wants to check in with you!:heart: Let "+message.author.name+" know how you are doing :hug:")
  elif message.content.startswith('.feeling'):
    emoji=(str(message.content))[8:]
    if message.author.name in arr:
      arr[message.author.name]+=emoji
    else:
      arr[message.author.name]=emoji
    await message.author.send("Thanks for sharing! Checkout your emojis from all your check-ins!:\n"+arr[message.author.name])
    print(message.content)
  print(arr)

client.run(os.getenv('TOKEN'))

