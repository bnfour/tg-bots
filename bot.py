# bot file
import telegram
from os import environ


class BotWrapper(object):
    # shh, it's a seecret
    TOKEN = environ['BNTGBOT_TOKEN']
    SERVER = environ['BNTGBOT_SERVER']
    # whenever bot is spoken to directly, it replies this
    REPLY_MSG = "I am an inline bot, please summon me elsewhere."

    # webhook is set there
    def __init__(self):
        self.bot = telegram.Bot(self.TOKEN)

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
        # button titles,
        titles = ("With spaces", "Compact without spaces")
        # descriptions,
        descs = ("Regular text.", "Uselful for long strings.")
        # and generated text - everything for the two variants
        msgs = (self.convert(text), self.convert_no_spaces(text))

        for t, d, m in zip(titles, descs, msgs):
            # first we indicate we use markdown in message that will be sent
            reply = telegram.InputTextMessageContent(m, parse_mode="Markdown")
            # then we generate result with that message and strings set above
            result = telegram.InlineQueryResultArticle(id=t, title=t,
                        description=d, input_message_content=reply)
            ret.append(result)
        return ret
