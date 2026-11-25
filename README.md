# Mira's Other Bot 
(aka Storyteller - it comes from the previous name "Haiku" and an OC of mine)

A discord bot that detects haikus and argues with you (sometimes)

Also he's got a ton of lore. Like, major-character-in-a-fanfiction amounts of lore. You can listen to some of it! (in poem form)

The bot is now hosted! For reasons known as "I'm literally just running a script on a server", the bot may go down now and then. It should get itself back up within the day though.

Updates on the bot will be pretty slow.

I may have used these external libraries:
- pyspellchecker
- nltk
- python-dotenv
- syllables
- requests
- discord.py

However, the list below is probably more accurate.

## Current Install Link
...is [this](https://discord.com/oauth2/authorize?client_id=1561063746883948686&permissions=412317240384&response_type=code&redirect_uri=https%3A%2F%2Fmirwx.neocities.org%2F&integration_type=0&scope=applications.commands+messages.read+bot)

Also theres a server with literally only the bot [here](https://discord.gg/hK3JjvADq)

Settings are now per-server!!

## To **Host** This Bot
I'll have an executable you can run to host in the future.

For now: Grab the source code.

Then, you need to install some libraries.
```bash
pip install nltk
pip install syllables
python3 -m pip install -U discord.py
# on windows, use the following rather than the former:
py -3 -m pip install -U discord.py
```

Open main.py and, somewhere below `# initializing` (but not before `# start/login stuff`), define a variable `TOKEN` with your bot token as a string.

You can also use a `.env` file instead. To do so, you also neeed to install dotenv.
```bash
pip install python-dotenv
```