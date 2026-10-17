import discord
import random as r
import os
from dotenv import load_dotenv
import resources.text_to_string as tts


# initializing
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# space for future variables & stuff
ANGLER = 1504819900957589555
FRIEDFISH = '<:friedfish:1561070704844341410>'
HELLOS = [
    'hihi',
    'hello!',
    'greetings'
]
COINS = ['1','0']


# start/login stuff
@client.event
async def on_ready():
    print(f"\033[93mWe have logged in as {client.user}")


# on message
@client.event
async def on_message(message):
    global last_sender

    # specifically for my one single tupperbox
    if message.author.id == ANGLER:
            await message.channel.send('shut up')
            await message.channel.send(f'give {last_sender.display_name} their message back smh')

    # ignores bot messages
    if message.author is client.user or message.author.bot:
        return

    # a greeting
    if 'hello' in message.content:
        await message.channel.send(r.choice(HELLOS))

    # specifically because my friends have beef with a fish
    if '1530253570996305940' in message.content:
        await message.channel.send('yes')
        await message.channel.send(FRIEDFISH)

    if '!flip' in message.content or '!coinflip' in message.content:
        await message.channel.send(r.choice(COINS))

    if '!help' in message.content:
        info = tts.stringify(tts.path)
        await message.channel.send(info)

    print(repr(message.author.id))
    last_sender = message.author

# running the bot
client.run(TOKEN)