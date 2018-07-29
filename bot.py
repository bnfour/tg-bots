# bot file
import telegram
from os import environ


class BotWrapper(object):
    # shh, it's a seecret
    TOKEN = environ['BNTGBOT_TOKEN']
    SERVER = environ['BNTGBOT_SERVER']
    # whenever bot is spoken to directly, it replies this
    REPLY_MSG = "I am an inline bot, please summon me elsewhere."

    # button titles
    titles = ("With spaces", "Compact without spaces")
    # and button descriptions
    descs = ("Regular text.", "Uselful for long strings.")

    # webhook is set there
    def __init__(self):
        self.bot = telegram.Bot(self.TOKEN)

        # urls to images for buttons, moved to constructor
        #  to reuse SERVER variable
        self.imgs = tuple(self.SERVER + i for i in ("/i/sparse.png", "/i/dense.png"))

        link = "https://{}/{}".format(self.SERVER, self.TOKEN)
        self.bot.set_webhook(url=link)

    # the handler for calls from telegram
    def web_hook(self, json):
        update = telegram.update.Update.de_json(json, self.bot)
        # this is primarily inline bot
        if update.message is not None:
            self.bot.send_message(chat_id=update.message.chat_id,
                                  text=self.REPLY_MSG)
        # inline stuff happens here
        elif update.inline_query is not None and len(update.inline_query.query) > 0:
            results = self.generate_inline_answer(update.inline_query.query)
            self.bot.answerInlineQuery(update.inline_query.id, results)

        return 'OK'

    # convert function #0, with spaces
    def convert(self, string):
        """
        "text" gets converted to
        T E X T
        E E
        X   X
        T     T
        """
        string = string.upper()
        ret = "```\n"
        ret += ' '.join(string) + "\n"
        for i, ch in enumerate(string[1::]):
            ret += ch + ' ' * (2 * i + 1) + ch + "\n"
        ret += "```"
        return ret

    # convert function #1, without spaces
    def convert_no_spaces(self, string):
        """
        "text" gets converted to
        TEXT
        EE
        X X
        T  T
        """
        string = string.upper()
        ret = "```\n"
        ret += string + "\n"
        for i, ch in enumerate(string[1::]):
            ret += ch + ' ' * i + ch + "\n"
        ret += "```"
        return ret

    # generates inline "buttons" via so-called article buttons
    def generate_inline_answer(self, text):
        ret = []
        # generated text - everything for the two variants
        #   rest of data to make the buttons moved to class declaration
        msgs = (self.convert(text), self.convert_no_spaces(text))

        for t, d, m, i in zip(self.titles, self.descs, msgs, self.imgs):
            # first we indicate we use markdown in message that will be sent
            reply = telegram.InputTextMessageContent(m, parse_mode="Markdown")
            # then we generate result with that message and strings set above
            result = telegram.InlineQueryResultArticle(id=t, title=t,
                        description=d, input_message_content=reply,
                        thumb_url=i, thumb_width=512, thumb_height=512)
            # thumb sizes above are hardcoded, as both pictures are 512×512
            #   a good approach is to actually load and measure them
            #   with pillow, for instance
            ret.append(result)
        return ret
