import discord
import random as r
import os
from dotenv import load_dotenv
import resources.text_to_string as tts
from resources.similar_string import *
import haiku_finder as h



# initializing
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



# space for future variables & stuff
ANGLER = 1504819900957589555
FRIEDFISH = '<:friedfish:1561070704844341410>'
HAIKU = '📃'
HELLOS = [
    'welcome',
    'hello!',
    'greetings',
    '...and how may I help you this fine new loop?'
]
HELLO_WEIGHTS = [
     3,
     2,
     2,
     0.1
]
COINS = ['1','0']



# defining embeds
info = discord.Embed(color=0xaab2b9, description=tts.stringify(tts.path), title="Commands")



# start/login stuff
@client.event
async def on_ready():
    print(f"\033[93mWe have logged in as {client.user}\033[0m")



# on message
@client.event
async def on_message(message):
    global last_sender
    global last_message

    # specifically for my one single tupperbox
    if message.author.id == ANGLER:
            if 'a:' in last_message.content.lower():
                # little condition since Angler has a prefix notation too
                await message.channel.send(f'give {last_sender.display_name} their message back smh')

            elif similar(last_message.content, message.content):
                await message.channel.send(f'give {last_sender.display_name} their message back smh')
            else:
                await message.channel.send('shut up')
                 

    # ignores bot messages
    if message.author is client.user or message.author.bot:
        return

    if_haiku = h.haiku_phrase(message.content)
    if if_haiku[0]:
         await message.add_reaction(HAIKU)
         await message.reply(if_haiku[1] + f'*- A haiku by {message.author.name}*')

    # a greeting
    if 'hello' in message.content:
        await message.channel.send(r.choices(HELLOS, weights=HELLO_WEIGHTS, k=1)[0])

    # specifically because my friends have beef with a fish
    if '1530253570996305940' in message.content:
        await message.channel.send('yes')
        await message.channel.send(FRIEDFISH)

    if '!flip' in message.content or '!coinflip' in message.content:
        await message.channel.send(r.choice(COINS))

    if '!setup' in message.content:
            await message.channel.send('OK! this is still WIP though.')

    if '!help' in message.content:
        #brb
        await message.channel.send('', embed=info)

    last_sender = message.author
    last_message = message



# running the bot
client.run(TOKEN)