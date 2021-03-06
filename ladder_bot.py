import telegram
import secrets
from bot_wrapper import BotWrapper


class LadderBot(BotWrapper):
    "Ladder bot, now with probably cleaner code!"
    token = secrets.LADDER_BOT_TOKEN
    inline_purpose = "ladder-like texts"

    def __init__(self):
        super().__init__()
        # button titles
        self.titles = ("With spaces", "Compact without spaces")
        # and button descriptions
        self.descs = ("Regular text.", "Uselful for long strings.")
        # and also thumbnails for those
        self.imgs = tuple(
            self.server + i for i in ("/i/sparse.png", "/i/dense.png"))

    def handle_message(self, message):
        "Responds to /start, nags to anything else."
        if message.text is not None and message.text == "/start":
            self.send_inline_start(message)
        else:
            self.send_inline_nag(message)
        return "OK"

    def handle_inline_query(self, inline_query):
        "Returns inline results."
        # skips empty messages
        if len(inline_query.query) > 0:
            results = self.generate_inline_answer(inline_query.query)
            self.bot.answer_inline_query(inline_query.id, results)
            return "OK"
        else:
            return "Empty message skip, kinda OK"

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

    def generate_inline_answer(self, text):
        "Generates inline 'buttons' via so-called article buttons."
        ret = []
        # generated text - everything for the two variants
        msgs = (self.convert(text), self.convert_no_spaces(text))
        for t, d, m, i in zip(self.titles, self.descs, msgs, self.imgs):
            # first we indicate we use markdown in message that will be sent
            r = telegram.InputTextMessageContent(m, parse_mode="Markdown")
            # then we generate result with that message and strings set above
            result = telegram.InlineQueryResultArticle(id=t, title=t,
                                                       description=d,
                                                       input_message_content=r,
                                                       thumb_url=i)
            ret.append(result)
        return ret
