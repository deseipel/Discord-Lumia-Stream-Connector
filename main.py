#requires Python 3.8+, discord.py, Lumiastream(running), a discord bot

#change log:
# 10.1.22 - initial release!  
#10.2.22  - addded $refresh function, so a restart shouldn't be needed when adding new commands

import discord
import aiohttp
import json
import asyncio

#in lumiastream, go to Settings->Api and copy your token in the lumiastreamTOKEN varaible
lumiastreamTOKEN = 'LUMIASTREAM TOKEN HERE'
lumiastreamURL = 'http://localhost:39231/api/send?token='
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
commands = []

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  await get_LScommands()


async def get_LScommands():
#get settings
  session = aiohttp.ClientSession()
  resp = await session.get('http://localhost:39231/api/retrieve?token=' + lumiastreamTOKEN)
  respdict = await resp.json()
  #dict type
  #print(respdict["data"]["options"]["chat-command"]["values"])
  global commands
  commands = respdict["data"]["options"]["chat-command"]["values"]
  #respjson = json.dumps(respdict, indent=4)
  print("These lumiastream commands were found",commands)
  await session.close()
  
async def eval_msg(wlist):
#sees if words are LS commands 
  #find all the words that start with an ! (could be multiple) and exclude the ! 
  matches = [ word.split("!")[1] for word in wlist if word.startswith('!') ]
    
  #print(matches)
  #print(commands) #this is not being set
  #find all the matches that are commands
  #if any((match := item) in matches for item in commands):
  #  print("these matched commandss",match)
  tosend = []
  for match in matches:
    for cmd in commands:
        if match == cmd:
            print("this is a lumiastream command: ",match)
            tosend.append(match)
            
       
  if  len(tosend)>0:        
    await post_LS(tosend)


async def post_LS(cmdlist):
    session = aiohttp.ClientSession()
    for x in cmdlist:    
        resp = await session.post(lumiastreamURL + lumiastreamTOKEN, json={ "type": "chat-command", "params": {"value": x} })
        respjson = await resp.json()
        #print(respjson)
    await session.close()   


  
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
  
  if message.content.startswith('$refresh'):
    await get_LScommands()
  
#if the message contains an exclamation point AND that word is a command, call it.
  #split the message into a list of words
  wordlist = message.content.split()
  #print(wordlist)
  await eval_msg(wordlist)
  
 
#do not share this discord bot token with anyone!
client.run(
  'BOT TOKEN HERE')
