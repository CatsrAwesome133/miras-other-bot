# Mira's Other Bot 
(aka Storyteller - it comes from the previous name "Haiku" and an OC of mine)

A discord bot that detects haikus and argues with you (sometimes)

Currently you can't just install the bot. It's very early in development and not hosted at all. If you want to you can get the code and host it yourself though.

I may have used these external libraries:
- pyspellchecker
- nltk
- python-dotenv
- syllables
- requests
- discord.py

However, the list below is probably more accurate.

## Current Install Link
...is [this](https://discord.com/oauth2/authorize?client_id=1561063746883948686&permissions=76864&response_type=code&redirect_uri=https%3A%2F%2Fmirwx.neocities.org%2F&integration_type=0&scope=messages.read+bot)

## To **Host** This Bot
You need to install some libraries.
```bash
pip install nltk
pip install python-dotenv
pip install syllables
python3 -m pip install -U discord.py
# on windows, use the following rather than the former:
py -3 -m pip install -U discord.py
```

You also need to setup a .env file with your bot token. It should look like this:
```
DISCORD_TOKEN=Your_Token_Here
```

In addition, you should replace `GUILD` in `constants.py` with your own server ID or change the following code in `main.py` in order for the bot to function.

Replacing `GUILD` will keep the bot commands functional only in the selected server, while changing the code will allow them to be exceuted from any server with the bot.
```py
# start/login stuff
@client.event
async def on_ready():
    print(f"\033[93mWe have logged in as {client.user}\033[0m")

    #-- GUILD COMMAND SYNCS FOR TESTING --#             # DELETE
    guild = discord.Object(id=GUILD)                    # THIS
    client.tree.copy_global_to(guild=guild)             # SECTION
    guild_sync = await client.tree.sync(guild=guild)    #
    print(f"Synced {len(guild_sync)} commands:")        #
    for cmd in guild_sync:                              #
        print(f" - {cmd.name}")                         #

    #-- GLOBAL COMMAND SYNCS, REPLACE GUILD SYNCS WHEN HOSTED --#
    #synced = await client.tree.sync()                   # REMOVE THE HASHTAGS
    #print(f"Synced {len(synced)} commands globally")    # FROM THIS
```

It should look like this when you're done.
```py
# start/login stuff
@client.event
async def on_ready():
    print(f"\033[93mWe have logged in as {client.user}\033[0m")

    #-- GLOBAL COMMAND SYNCS, REPLACE GUILD SYNCS WHEN HOSTED --#
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} commands globally")
```