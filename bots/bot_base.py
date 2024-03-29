import atexit
import telegram

from bottle import HTTPResponse
from typing import Iterable

from .bot_info import BotInfo


class BotBase(object):
    "An 'abstract' class to reuse code between different bots in this app."
    # should complete "to get a propmpts for [inline_purpose]"
    inline_purpose = "ERROR"

    def __init__(self, server: str, token: str | None, admins: Iterable[int]):
        "Common setup happens here."

        self.server = server
        self.token = token
        self.admins = admins

        if self.is_active():
            self.bot = telegram.Bot(self.token)
            # please note HTTPS is enforced
            webhook_url = f"https://{self.server}/{self.token}"
            self.bot.set_webhook(url=webhook_url)

            atexit.register(self.cleanup)

    def cleanup(self) -> None:
        "Cleanup method to remove the webhook on exit for additional tidiness."
        self.bot.delete_webhook()

    def is_active(self) -> bool:
        "A check whether is bot is configured to be active by providing a non-empty token"
        # imagine using js-like !! shenanigans
        return not not self.token

    def get_data(self) -> BotInfo:
        "Returns general bot info for display"
        is_active = self.is_active()
        name = self.bot.get_me().username if is_active \
            else None
        return BotInfo(is_active, name)

    def handle_update(self, update_as_json: str) -> HTTPResponse:
        """
        Routes updates to relevant methods.
        Supports only direct messages and inline queries.
        """
        # should never happen, as without token this will not be called
        # let's return the teapot code anyway
        if not self.is_active():
            return HTTPResponse(status=418)

        update: telegram.Update = telegram.Update.de_json(update_as_json, self.bot)
        if update.message is not None:
            return self.handle_message(update.message)
        elif update.inline_query is not None:
            return self.handle_inline_query(update.inline_query)
        else:
            # ignore all other updates, but still respond to the request
            return HTTPResponse(status=200)

    def handle_message(self, message: telegram.Message) -> HTTPResponse:
        "Should be overriden to handle incoming messages."
        pass

    def handle_inline_query(self, inline_query: telegram.InlineQuery) -> HTTPResponse:
        "Should be overriden to handle incoming inline queries."
        pass

    def is_token(self, maybe_token: str) -> bool:
        "Checks whether provided string is indeed token of this bot"
        return maybe_token == self.token

    def is_message_from_admin(self, message: telegram.Message) -> bool:
        "Checks whether a direct message comes from an admin of this app."
        if message.from_user is None:
            return False
        id_from = message.from_user.id
        return id_from in self.admins

    def reply(self, message: telegram.Message, text: str) -> None:
        "Convenience method to be repeteadly called within the bots."
        self.bot.send_message(chat_id=message.chat_id, text=text)

    def send_inline_nag(self, message: telegram.Message) -> None:
        """
        Default reply of ladder bot, now promoted to common method.
        Also a way to test whether 'admin' code works.
        """
        reply_text = "Hello boss." if self.is_message_from_admin(message) \
            else "I'm an inline bot, please summon me elsewhere."
        self.reply(message, reply_text)

    def send_inline_start(self, message: telegram.Message) -> None:
        """
        Default reply of inline bots to /start command.
        Briefly informs user on what this bot can do.
        """
        my_name = self.bot.get_me().username
        reply_text = "Hi there!\nI'm an inline bot, so feel free to summon" +\
            f" me in other chats as\n@{my_name} sample text\nto" +\
            f" get prompts for {self.inline_purpose}."
        self.reply(message, reply_text)
