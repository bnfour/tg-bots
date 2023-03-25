from bottle import HTTPResponse

import config_secrets

from .bot_info import BotInfo
from .ladder_bot import LadderBot
from .cat_macro_bot import CatMacroBot

class BotManager(object):
    "Incapsulates all interaction with BotBase descendants."

    def __init__(self):
        self._bots = (
            LadderBot(config_secrets.SERVER, config_secrets.LADDER_BOT_TOKEN, config_secrets.ADMINS),
            CatMacroBot(config_secrets.SERVER, config_secrets.CAT_MACRO_BOT_TOKEN, config_secrets.ADMINS)
        )
        # actual bot info, and an empty value to generate a placeholder
        self._info: tuple[BotInfo] = tuple([bot.get_data() for bot in self._bots] + [BotInfo.get_placeholder_info(),])

    def get_info(self) -> tuple[BotInfo]:
        "Returns info about configured bots, and a placeholder value"
        # TODO wait, why it returns the placeholder here?
        return self._info

    def handle_request(self, token: str, body: str) -> HTTPResponse:
        "Calls a bot by its token, or returns 404 for unknown value"
        for bot in self._bots:
            if bot.is_active() and bot.is_token(token):
                try:
                    return bot.handle_update(body)
                except:
                    return HTTPResponse(status=500)
        else:
            return HTTPResponse(status=404)
