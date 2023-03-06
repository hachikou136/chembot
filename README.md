# Chembot

This repository is forked from Chembot🐙

And the bot is available on [chembot - Replit](https://replit.com/@hachikou136/chembot)💪

Chembot is a chemistry discord bot built on the Python package [chemlib](https://github.com/chemlib/chemlib) that provides easy access to element data and quickly performs calculations.

## main points fixed from origin repository🛠

Mainly changed to accommodate changing specification after discord.py version 2.0.

1. dealt with changing specification about intents after discord.py version 2.0.(ref: [what does 'TypeError: BotBase.__init__() missing 1 required keyword-only argument: 'intents'' mean and how do i fix it : discordbots](https://www.reddit.com/r/discordbots/comments/x6ljgk/what_does_typeerror_botbase_init_missing_1/))
2. dealt with changing specification about a method `Bot.load_extension` after discord.py version 2.0.(ref: [python - "RuntimeWarning: coroutine 'BotBase.load_extension' was never awaited" after updating discord.py - Stack Overflow](https://stackoverflow.com/questions/71504627/runtimewarning-coroutine-botbase-load-extension-was-never-awaited-after-upd))
3. fixed to keep alive the bot to work at replit.
4. stopped loading an extension `quiz.py`, because the extension did not work by an error about PyPDF.
5. stopped using a file `token.txt` to set bot token for security reason to work as replit machine. and, using an environment variable via a replit feature `secret` instead.

## check the bot status🤖

[my-bots-status](https://stats.uptimerobot.com/ODYmKHNjr6)

## Commands

**Command Prefix: ``-``**

### help

Displays help message.

Usage: ``-help``

![help](https://user-images.githubusercontent.com/58019082/104853716-7f201300-58b7-11eb-9e6e-c697b32e18e0.jpg)

### elem 

Displays properties of requested element by symbol.

Usage: ``-elem <symbol>``

![elements](https://user-images.githubusercontent.com/58019082/104853737-ad9dee00-58b7-11eb-86a0-b734113fcf2f.jpg)

### cmpd

Gets the molar mass of a compound, and performs optional calculations.

Usage: ``-cmpd <formula>``

Additional Parameters (accepts abbreviations): 
- ``--amount <number and units>``
- ``--composition <elem symbol>``

![cmpd](https://user-images.githubusercontent.com/58019082/104853774-e5a53100-58b7-11eb-881a-bd04ad914020.jpg)