import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

client = discord.Client()

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there!",
  "You are an amazing person!",
  "Smile please :-)"
]

if "responding" not in db.keys():
  db["responding"]= True

def get_quote():
  response = requests.get("https://type.fit/api/quotes")
  json_data = json.loads(response.text)
  n = random.randint(0,1643)
  quote = json_data[n]['text'] + "\n ~" + json_data[n]['author']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send(
    "Hello {0}!".format(message.author))

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg.lower() for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$add"):
    encouraging_message = msg.split("$add ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added!")
  
  if msg.startswith("$delete"):
    encouragements=[]
    if "encouragements" in db.keys():
      index = int(msg.split("$delete", 1)[1])
      delete_encouragement(index)
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on!")
    else:
      db["responding"] = False
      await message.channel.send("Responsding is off!")

keep_alive()
client.run(os.getenv('TOKEN'))

