import telegram

from bottle import HTTPResponse
from typing import List, Iterable

from bot_wrapper import BotWrapper


class LadderBot(BotWrapper):
    "Ladder bot, now with probably cleaner code!"
    inline_purpose = "ladder-like texts"
    # button titles
    titles = ("With spaces", "Compact without spaces")
    # and button descriptions
    descs = ("Regular text.", "Uselful for long strings.")

    def __init__(self, server: str, token: str, admins: Iterable[int]):
        super().__init__(server, token, admins)
        # populate inline options' URL once the server is known
        self.imgs = tuple(self.server + i for i in ("/i/sparse.png", "/i/dense.png"))

    def handle_message(self, message: telegram.Message) -> HTTPResponse:
        "Responds to /start, nags to anything else."
        if message.text is not None and message.text == "/start":
            self.send_inline_start(message)
        else:
            self.send_inline_nag(message)

        return HTTPResponse(body="OK", status=200)

    def handle_inline_query(self, inline_query: telegram.InlineQuery) -> HTTPResponse:
        "Returns inline results."
        # skips empty messages
        if len(inline_query.query) > 0:
            results = self.generate_inline_answer(inline_query.query)
            self.bot.answer_inline_query(inline_query.id, results)
            return HTTPResponse(body="OK", status=200)
        else:
            return HTTPResponse(body="Query empty", status=200)

    # convert function #0, with spaces
    def convert(self, text: str) -> str:
        """
        "text" gets converted to
        T E X T
        E E
        X   X
        T     T
        """
        text = text.upper()
        ret = "```\n"
        ret += ' '.join(text) + "\n"
        for i, ch in enumerate(text[1::]):
            ret += ch + ' ' * (2 * i + 1) + ch + "\n"
        ret += "```"
        return ret

    # convert function #1, without spaces
    def convert_no_spaces(self, text: str) -> str:
        """
        "text" gets converted to
        TEXT
        EE
        X X
        T  T
        """
        text = text.upper()
        ret = "```\n"
        ret += text + "\n"
        for i, ch in enumerate(text[1::]):
            ret += ch + ' ' * i + ch + "\n"
        ret += "```"
        return ret

    def generate_inline_answer(self, text: str) -> List[telegram.InlineQueryResultArticle]:
        "Generates inline 'buttons' via so-called article buttons."
        ret: List[telegram.InlineQueryResultArticle] = []
        # generated text - everything for the two variants
        msgs = (self.convert(text), self.convert_no_spaces(text))
        for t, d, m, i in zip(self.titles, self.descs, msgs, self.imgs):
            # first we indicate we use markdown in message that will be sent
            r = telegram.InputTextMessageContent(m, parse_mode="Markdown")
            # then we generate result with that message and strings set above
            result = telegram.InlineQueryResultArticle(id=t, title=t,
                description=d, input_message_content=r, thumb_url=i)
            ret.append(result)
        return ret
