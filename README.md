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

However, the list below is probably more accurate.

## Current Install Link
...is [this](https://discord.com/oauth2/authorize?client_id=1561063746883948686&permissions=76864&response_type=code&redirect_uri=https%3A%2F%2Fmirwx.neocities.org%2F&integration_type=0&scope=messages.read+bot)

## To **Host** This Bot
You need to install some libraries.
```bash
pip install nltk
pip install python-dotenv
pip install syllables
```

You also need to setup a .env file with your bot token. It should look like this:
```
DISCORD_TOKEN=Your_Token_Here
```