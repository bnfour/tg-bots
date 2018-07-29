# bnfour's telegram bot(s)
Currently there is source for one telegram bot.
## Ladder bot (officially hosted as [@bnladder_bot](https://t.me/bnladder_bot))
Inline bot that generates texts running along horizontal, vertical and diagonal directions, for instance:

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

Yup, pretty useless.

### Deployment
Dependencies:
* [bottle](https://pypi.python.org/pypi/bottle/0.12.13)
* [telegram-python-bot](https://pypi.python.org/pypi/python-telegram-bot/10.0.1)

You'll need to provide some kind of SSL-proxy to the bottle app used to host the bot (`nginx` will do nicely). Token and server are set as environment variables `BNTGBOT_TOKEN` and `BNTGBOT_SERVER` respectively.

If your server supports `systemd` like mine does, [here's](https://gist.github.com/bnfour/1ebcc358e70053d309b5137eae3d1cc9) how I set up this as a service.

### Credits
* Avatar was a [CC0 photo](https://www.publicdomainpictures.net/view-image.php?image=236923&picture=cat-with-blue-eyes) until I decided to reuse newly introduced picture for "With spaces button".

* The whole endeavor is loosely inspired by [this fine article](https://hackernoon.com/host-a-python-telegram-bot-using-azure-in-30-minutes-58f246cedf23).