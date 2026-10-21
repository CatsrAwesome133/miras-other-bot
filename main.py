import discord
from discord import app_commands
from typing import Literal, Optional
import random as r
import os
from dotenv import load_dotenv
import resources.text_to_string as tts
from resources.similar_string import *
from resources.metric import metric
from constants import *
import haiku_finder as h



# command setup
class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

# initializing
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
target = ANGLER

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)



# defining embeds
setup_text = ""
info = discord.Embed(color=0xaab2b9, description=tts.stringify(tts.path), title="Commands")
setup_info = discord.Embed(color=0xaab2b9, description=setup_text, title="You've changed these settings:")



# start/login stuff
@client.event
async def on_ready():
    guild = discord.Object(id=GUILD)
    client.tree.copy_global_to(guild=guild)

    print(f"\033[93mWe have logged in as {client.user}\033[0m")

    guild_sync = await client.tree.sync(guild=guild)
    print(f"Synced {len(guild_sync)} commands:")
    for cmd in guild_sync:
        print(f" - {cmd.name}")
    
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} commands globally")



# on message
@client.event
async def on_message(message):
    global last_sender
    global last_message

    # specifically for my one single tupperbox
    if message.author.id == target:
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
        await message.channel.send('Sorry, this is not the correct command. Please use `/setup` instead!')

    if '!help' in message.content:
        #brb
        await message.channel.send('', embed=info)

    if '!metricthis' in message.content or 'imnotamerican' in "".join([c for c in message.content.lower() if c.isalpha()]):
        pass

    if any(key in message.content for key in c):
        converted = metric(message.content, "you")
        await message.channel.send(converted[0])
        if converted[1]:
            await message.channel.send("I am confused too.")

    last_sender = message.author
    last_message = message



# commands
@client.tree.command()
@app_commands.describe(
    beef_at='By default this bot hates the Angler. Change this here.',
    beef_at_id= "You can also use the target's user ID",
)
async def setup(
    interaction: discord.Interaction,
    beef_at: Optional[discord.User],
    beef_at_id: Optional[int],
):
    """Some configuration options for the bot"""
    global target

    if beef_at:
        target = beef_at.id

    if beef_at_id:
        target = beef_at_id
    
    await interaction.response.send_message('', embed=setup_info, ephemeral=False)


@client.tree.command()
async def help(
    interaction: discord.Interaction,
):
    """Shows a list of commands and other helpful stuff"""
    global setup_text
    await interaction.response.send_message('', embed=info, ephemeral=False)



# running the bot
client.run(TOKEN)