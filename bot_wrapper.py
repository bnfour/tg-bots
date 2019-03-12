import telegram
import secrets


class BotWrapper(object):
    "An 'abstract' class to reuse code between different bots in this app."
    # should be overriden in actual bots
    token = ""
    server = secrets.SERVER
    # should complete "to get a propmpts for [inline_purpose]"
    inline_purpose = "ERROR"

    def __init__(self):
        "Common setup happens here."
        self.bot = telegram.Bot(self.token)

        webhook_url = f"https://{self.server}/{self.token}"
        self.bot.set_webhook(url=webhook_url)

    def handle_update(self, update_as_json):
        """
        Routes updates to relevant methods.
        Supports only direct messages and inline queries.
        """
        update = telegram.update.Update.de_json(update_as_json, self.bot)
        if update.message is not None:
            return self.handle_message(update.message)
        elif update.inline_query is not None:
            return self.handle_inline_query(update.inline_query)

    def handle_message(self, message):
        "Should be overriden to handle incoming messages."
        pass

    def handle_inline_query(self, inline_query):
        "Should be overriden to handle incoming inline queries."
        pass

    def is_token(self, string):
        "Checks whether provided string is indeed token of this bot"
        return string == self.token

    def is_message_from_admin(self, message):
        "Checks whether a direct message comes from an admin of this app."
        if message.from_user is None:
            return False
        id_from = message.from_user.id
        return id_from in secrets.ADMINS

    def send_inline_nag(self, message):
        """
        Default reply of ladder bot, now promoted to common method.
        Also a way to test whether 'admin' code works.
        """
        reply_text = "Hello boss." if self.is_message_from_admin(message) \
            else "I'm an inline bot, please summon me elsewhere."
        self.bot.send_message(chat_id=message.chat_id, text=reply_text)

    def send_inline_start(self, message):
        """
        Default reply of inline bots to /start command.
        Briefly informs user on what this bot can do.
        """
        my_name = self.bot.get_me().username
        reply_text = "Hi there!\nI'm an inline bot, so feel free to summon" +\
            f" me in other chats as\n@{my_name} sample text\nto get prompts" +\
            f" for {self.inline_purpose}."
        self.bot.send_message(chat_id=message.chat_id, text=reply_text)
