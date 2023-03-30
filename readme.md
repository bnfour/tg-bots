# bnfour's (python) telegram bot(s)
Disclaimer: this was written back in 2018, and does not work with the latest async-based version of the Telegram wrapper library used within. I can't be bothered to rewrite this and/or change the library to use, so take this code with a grain of salt.

Currently there is source for two (very-very-ultra useful) telegram bots.

## Ladder bot (officially hosted as [@bnladder_bot](https://t.me/bnladder_bot))
Inline bot that generates texts running along horizontal, vertical and diagonal directions simultaneously, for instance:

`@bnladder_bot sample text` generates prompts for two messages:
1. With spaces:
```
S A M P L E   T E X T
A A
M   M
P     P
L       L
E         E

T             T
E               E
X                 X
T                   T
```
2. Without spaces:
```
SAMPLE TEXT
AA
M M
P  P
L   L
E    E

T      T
E       E
X        X
T         T
```

## Cat macro bot (officially hosted as [@bncatpics_bot](https://t.me/bncatpics_bot))
Inline bot that can be used to post any pictures searchable by defined captions. I use it to store and post cat pictures I used to spam before I moved to Telegram and started spamming stickers.  
Here's an example screenshot:  
![also pictured: fancy car](https://i.imgur.com/uDQmbxa.png)  

You can also try searching for stuff like `cat tech` or `bread` to see the outstanding quality of the pictures I hoarded.

### Usage
This bot isn't strictly inline: administrator accounts can manage pictures via chatting:
* Sending a captioned photo will add that photo and make it searchable by provided caption.
* `/delete` (or anything starting with `/delet`) puts bot into deletion mode: next picture to be sent (try to forward actual bot output) will be deleted from the collection if present. Anything else just cancels the deletion mode.

## Deployment
See `requirements.txt` for dependencies. `python-Levenshtein` is optional and may be removed, although `fuzzywuzzy` will tell you to install it for performance reasons.

Configuration, including tokens for both bots and list of admin accounts, is stored in `config_secrets.py` file. This file is not tracked in this repo, so you can edit it without accidentally committing debug or even production configs for the world to see.

See provided `config_secrets.example.py` for a list of things this file should define.

You'll need to provide some kind of SSL-proxy to the bottle app used to host the bots (`nginx` will do nicely). 
