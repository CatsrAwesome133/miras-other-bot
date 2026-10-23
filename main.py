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
info = discord.Embed(color=0xaab2b9, description=tts.stringify(tts.path), title="Commands")



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
                await message.channel.send(r.choice(give_msg_back(last_sender.display_name)))

            elif similar(last_message.content, message.content):
                await message.channel.send(r.choice(give_msg_back(last_sender.display_name)))

            elif 'hey' in message.content.lower():
                await message.channel.send('"Hey" you!')

            elif 'shut up' in message.content.lower():
                await message.channel.send('*You* should shut up.')

            elif 'what' in message.content.lower():
                await message.channel.send('What?')

            elif 'stop' in message.content.lower():
                await message.channel.send('You first!')

            else:
                if r.random() < 0.2:
                    await message.channel.send('Shut up.')
                 

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

    if '!filp' in message.content:
            await message.channel.send("I'm sorry, but our coins don't filp.")

    if '!setup' in message.content:
        await message.channel.send('Sorry, this is not the correct command. Please use `/setup` instead.')

    if '!help' in message.content:
        await message.channel.send('', embed=info)

    if '!metricthis' in message.content or 'imnotamerican' in "".join([c for c in message.content.lower() if c.isalpha()]):
        pass

    if r.random() < 0.001:
        await message.channel.send(r.choice(FUN))

    if any(key in message.content for key in c):
        converted = metric(message.content, "you")
        if converted[2] != []:
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
    global setup_text

    if beef_at:
        target = beef_at.id
        setup_text = f'**Beef at:** <@{target}>'

    if beef_at_id:
        target = beef_at_id
        setup_text = f'**Beef at:** <@{target}>'
    
    setup_info = discord.Embed(color=0xaab2b9, description=setup_text, title="You've changed these settings:")
    await interaction.response.send_message('', embed=setup_info, ephemeral=False)


@client.tree.command()
async def help(
    interaction: discord.Interaction,
):
    """Shows a list of commands and other helpful stuff"""
    global setup_text
    await interaction.response.send_message('', embed=info, ephemeral=False)


@client.tree.command()
async def story(
    interaction: discord.Interaction,
    choice: Literal["My homeland", "That mountain called Apotheosis", "Warrior of the Seas", "Muse of the Skies", "The Creator"]
):
    """Hear about our stories"""
    siren = discord.Embed(color=0xaab2b9, description="A terror, a gale.\nA kind mother.\nBut many would dispute that.\n\n" \
                                                    "Once she found a pair of twins in the sky.\nThey ran, and I never found out why.\nI hear they live today, running about doing void knows what.", title="Siren of the Seas")
    storyteller = discord.Embed(color=0xaab2b9, description="Singer-Storyteller: Long-dead and long-forgotten, \nthough I recall \na little moth singing about me.\n\n" \
                                                    "Fly in the skies and a visage may show.\nBut who you see you shall never know.", title="I'm irrelevant.")
    mira = discord.Embed(color=0xaab2b9, description="She's an interesting one.\nA bird who never flies,\nExcept in the mind's eye.\n\n" \
                                                    "Speak your dreams, and\nWrite our tales.\nYou may find them here.", title="A Sparrow who draws")

    if choice == 'Warrior of the Seas':
        await interaction.response.send_message('You want to hear about her? Alright.', embed=siren, ephemeral=False)
    if choice == 'Muse of the Skies':
        await interaction.response.send_message('You want to hear about me?', embed=storyteller, ephemeral=False)
    if choice == 'The Creator':
        await interaction.response.send_message('Oh, them.', embed=mira, ephemeral=False)

@client.tree.command()
async def do_you_have_a_map(
    interaction: discord.Interaction,
):
    """He could have a map."""
    await interaction.response.send_message('I have no navigaton tool nor multi-animator project.', ephemeral=False)

@client.tree.command()
async def not_even_a_compass(
    interaction: discord.Interaction,
):
    """Really though?"""
    await interaction.response.send_message('No.', ephemeral=False)



# running the bot
client.run(TOKEN)