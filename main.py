import discord, os
from discord import app_commands
from typing import Literal, Optional
import random as r
import json
from dotenv import load_dotenv
from datetime import datetime, UTC
import sqlite3
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

def fetch_settings(output):
    conn = sqlite3.connect("settings.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS screw_it (
            id INTEGER PRIMARY KEY,
            guild INTEGER,
            target TEXT,
            random_freq DOUBLE,
            metric_chance DOUBLE
        );'''
    )


    ''' add a row
    cursor.execute(
        "INSERT INTO settings (guild, target, random_freq, metric_chance) VALUES (?, ?, ?, ?)",
        (0, 0, 0.1, 0.1)
    )
    '''

    cursor.execute(f"SELECT * FROM {TABLE}") # switch to settings later

    rows = cursor.fetchall() # list of tuples? [(1, 0, 0, 0.1, 0.1)]
    settings = {row["guild"]: dict(row) for row in rows}

    if output:
        print(settings)

    conn.commit()
    conn.close()

    return settings


# initializing
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# TOKEN = input("Bot Token: ")

with open('resources/tales.json', 'r') as f:
    TALES = json.load(f)

settings = fetch_settings(True)

last_status = ""

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)



# defining embeds
info = discord.Embed(color=0xaab2b9, description=tts.stringify(tts.path), title="Commands")



# start/login stuff
@client.event
async def on_ready():
    print(f"\033[93mWe have logged in as {client.user}\033[0m")

    #-- GUILD COMMAND SYNCS FOR TESTING --#
    # guild = discord.Object(id=GUILD)
    # client.tree.copy_global_to(guild=guild)
    # guild_sync = await client.tree.sync(guild=guild)
    # print(f"Synced {len(guild_sync)} commands:")
    # for cmd in guild_sync:
    #     print(f" - {cmd.name}")

    #-- GLOBAL COMMAND SYNCS --#
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} commands globally")


############# STATUSES #########################################
### 'h'     Haiku                                            ###
### 'i'     Just introduced                                  ###
### 'a'     Archives "Easter Egg"                            ###
### 'm'     Last message was sent by this bot                ###
################################################################

# on message
@client.event
async def on_message(message):
    global last_sender
    global last_message
    global last_status
    global settings


    try: 
        target = settings[message.guild.id]['target']
    except KeyError:
        target = str(ANGLER)

    try:
        metric_chance = settings[message.guild.id]['metric_chance']
    except KeyError:
        metric_chance = 0.8

    try:
        random_freq = settings[message.guild.id]['random_freq']
    except KeyError:
        random_freq = 0.005

    # ignores the bot return so beef with other bots works
    if message.author.id == target:
            # little condition since Angler has a prefix notation too
            if 'a:' in last_message.content.lower():
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
                elif r.random() < 0.2:
                    await message.channel.send('Tsk.')
                 

    # ignores bot messages
    if message.author is client.user or message.author.bot:
        return

    # because he's the god of the sky lol
    if message.content.strip().lower() == 'sky':
        await message.channel.send('Yes?')

    # orpheus inspired me
    if last_status == 'h' and any (i in message.content.lower() for i in THANKS):
        await message.channel.send(r.choice(YOURE_WELCOME))
    global this
    try:
        if this.author == client.user and any (i in message.content.lower() for i in THANKS):
            await message.channel.send(r.choice(YOURE_WELCOME))
    except NameError:
        pass
    this = message
    
    # haiku detector
    if_haiku = h.haiku_phrase(message.content)
    if if_haiku[0]:
        await message.add_reaction(HAIKU)
        await message.reply(if_haiku[1] + f'*- A haiku by {message.author.display_name}*')
        last_status = 'h'
    else:
        last_status = ''

    # a greeting
    if 'hello' in message.content:
        await message.channel.send(r.choices(HELLOS, weights=HELLO_WEIGHTS, k=1)[0])

    # specifically because my friends have beef with a fish
    if '1530253570996305940' in message.content:
        await message.channel.send('yes')
        await message.channel.send(FRIEDFISH)

    # non-slash commandss
    if '!flip' in message.content or '!coinflip' in message.content:
        await message.channel.send(r.choice(COINS))

    if '!filp' in message.content:
            await message.channel.send("I'm sorry, but our coins don't filp.")

    if '!setup' in message.content:
        await message.channel.send('Sorry, this is not the correct command. Please use `/setup` instead.')

    if '!help' in message.content:
        await message.channel.send('', embed=info)

    if '!metricthis' in message.content or 'imnotamerican' in "".join([c for c in message.content.lower() if c.isalpha()]):
        converted = metric(last_message.content, "they")
        if converted[2] != []:
            await message.channel.send(converted[0])
            if converted[1]:
                await message.channel.send("I am confused too.")
        else:
            await message.channel.send("I do not see any units...")

    if '!settings' in message.content:
        embed = discord.Embed(color=0xaab2b9, description=f"**Beefing at:** <@{target}>\n**Random messages:** every {round(1/random_freq)} messages\n**Randomize metric conversions:** {metric_chance >= 1}\n**Metric conversions:** {metric_chance > 0}", title="Current settings:")
        await message.channel.send("", embed=embed)

    if '' in message.content:
        time = datetime.now(UTC)

    # introduction
    if any (i in message.content for i in INTRO):
            await message.channel.send("Hello! I am the Singer-Storyteller, but you can just call me Storyteller. Or Haiku, if you would like an in-joke! I prefer he/him, but I *am* a discord bot, so feel free to use it/its as well. The Sparrow made me to die, but I live on in their computer. Ha!\n" \
                                        "As a bot, I look around the server for haikus and chat sometimes! There's also this one fish... \n" \
                                        "-# Use `!help` to find out more.")
            last_status = "i"

    # random messages for funsies
    if r.random() < random_freq:
        await message.channel.send(r.choice(FUN))

    # conversation regarding the Archives
    if "the archive" in message.content.lower():
        await message.channel.send("What archives?")
        last_status = 'a0'
    # resets the status
    elif last_status == 'a0': 
        last_status = ''

    if ("you know the one" in message.content.lower() or "you know" in message.content.lower() or "yk the one" in message.content.lower()) and last_status == "a0":
            await message.channel.send("I do not beleive so?")
            last_status = ''

    # auto metric conversion
    if any(key in message.content for key in c) and r.random() <= metric_chance:
        print('yep converting')
        converted = metric(message.content, "you")
        if converted[2] != []:
            await message.channel.send(converted[0])
            if converted[1]:
                await message.channel.send("I am confused too.")
            if r.random() < 0.1:
                await message.channel.send("If that didn't contain units, my greatest apologies. We are not that smart.")


    last_sender = message.author
    last_message = message



# commands
@client.tree.command()
@app_commands.describe(
    beef_at='By default this bot hates the Angler. Change this here.',
    beef_at_id= "You can also use the target's user ID.",
    convert_to_metric='Wether or not to automatically convert messsages with units to metric',
    random_message_frequency='How often the bot sends random messages, in chance per message. Default 0.005, please enter a decimal chance.',
)
async def setup(
    interaction: discord.Interaction,
    beef_at: Optional[discord.User],
    beef_at_id: Optional[str],
    convert_to_metric: Optional[Literal["Always", "Randomized", "Never Automatically"]],
    random_message_frequency: Optional[float],
):
    """Some configuration options for the bot"""
    global settings

    # Fetching current/default values
    try: 
        target = settings[interaction.guild.id]['target']
    except KeyError:
        target = str(ANGLER)

    try:
        metric_chance = settings[interaction.guild.id]['metric_chance']
    except KeyError:
        metric_chance = 0.8

    try:
        random_freq = settings[interaction.guild.id]['random_freq']
    except KeyError:
        random_freq = 0.005

    setup_text = ''

    conn = sqlite3.connect("settings.db")
    cursor = conn.cursor()

    if beef_at:
        target = beef_at.id
        setup_text += f'**Beef at:** <@{target}>'

    if beef_at_id:
        if len(beef_at_id) == 18 or len(beef_at_id) == 19:
            try:
                target = int(beef_at_id)
                setup_text = f'**Beef at:** <@{target}>\n'
            except ValueError:
                await interaction.response.send_message('That is not a valid user ID.', ephemeral=True)
                return

    if convert_to_metric is not None:
            if convert_to_metric == "Always":
                metric_chance = 1
            elif convert_to_metric == "Never Automatically":
                metric_chance = 0
            elif convert_to_metric == "Randomized":
                metric_chance = 0.8
            
            setup_text += f'**Convert imperial to metric:** {convert_to_metric}\n'

    if random_message_frequency:
        if random_message_frequency < 1:
            random_freq = random_message_frequency
            setup_text += f'**Random message every:** {round(1/random_freq)} messages\n'
        else:
            await interaction.response.send_message('Random message frequency must be a decimal smaller than 1', ephemeral=True)
            return
    
    cursor.execute(f"SELECT * FROM {TABLE} WHERE guild = ?", (interaction.guild.id,))

    rows = cursor.fetchall() # list of tuples? [(1, 0, 0, 0.1, 0.1)]

    if rows == []:
        cursor.execute(
            f"INSERT INTO {TABLE} (guild, target, random_freq, metric_chance) VALUES (?, ?, ?, ?)",
            (interaction.guild.id, target, random_freq, metric_chance)
        )
    else:
        cursor.execute(
            f'''UPDATE {TABLE}
            SET target = ?, random_freq = ?, metric_chance = ?
            WHERE guild = ?; ''',
            (target, random_freq, metric_chance, interaction.guild.id)
        )

    conn.commit()
    conn.close()

    settings = fetch_settings(True)
    
    setup_text = setup_text.strip('\n')
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
async def flip(
    interaction: discord.Interaction,
):
    """Flip a coin"""
    await interaction.response.send_message(r.choice(COINS), ephemeral=False)


@client.tree.command()
@app_commands.choices(
    choice=[
        app_commands.Choice(name=i["option"], value=i["option"])
        for i in TALES
    ]
)
async def story(
    interaction: discord.Interaction,
    choice: app_commands.Choice[str]
):
    
    """Hear about our stories"""
    # Monitoring the input ahsdkfeljb
    chosen = False

    for opt in TALES:
        if choice.value == opt["option"]:
            embed = discord.Embed(color=0xaab2b9, description="\n".join(opt["poem"]), title=opt["title"])
            await interaction.response.send_message(opt["comment"], embed=embed, ephemeral=False)
            chosen = True
    if not chosen:
        await interaction.response.send_message('Invalid option', ephemeral=True)

    
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