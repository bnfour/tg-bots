import telegram
import os
import json
from fuzzywuzzy import fuzz

import secrets
from bot_wrapper import BotWrapper


class CatMacroBot(BotWrapper):
    "Class for inline searches of predefined collection of pictures"
    token = secrets.CAT_MACRO_BOT_TOKEN
    inline_purpose = "matching cat pictures"
    # path to physical backup of available pictures
    file_path = "data/cat_pics.json"
    # up to this amount of somewhat relevant pics will be served
    max_pics = 7

    def __init__(self):
        super().__init__()
        # data is dict macro text -> Telegram media id to send
        self.data = None
        # loading of exisiting data
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.data = json.load(file)
        else:
            self.data = dict()
        # used to keep track of whether admins issued /delete commands
        self.deletion_tracker = {admin: False for admin in secrets.ADMINS}

    def handle_message(self, message):
        "Responds to /start, also adds pictures from admins to collection."
        if message.text is not None and message.text == "/start":
            self.send_inline_start(message)
        elif self.is_message_from_admin(message):
            admin_id = message.from_user.id
            if self.deletion_tracker[admin_id]:
                return self.handle_deletion_admin_input(message, admin_id)
            else:
                return self.handle_regular_admin_input(message, admin_id)
        else:
            self.send_inline_nag(message)
        return "OK"

    def handle_inline_query(self, inline_query):
        "Returns inline results."
        results = self.generate_inline_results(inline_query.query)
        self.bot.answer_inline_query(inline_query.id, results)
        return "OK"

    def generate_inline_results(self, query):
        "Generates inline answers as pictures."
        inline_results = []
        for ans_id, media_id in enumerate(self.find_most_relevant_pics(query)):
            r = telegram.InlineQueryResultCachedPhoto(ans_id, media_id)
            inline_results.append(r)
        return inline_results

    def find_most_relevant_pics(self, query):
        "Finds up to max_pics results and returns them as tuple of media ids"
        results = []
        if len(query) < 3:
            return results
        for caption in self.data:
            ratio = fuzz.partial_ratio(query, caption)
            if ratio > 50:
                results.append((self.data[caption], ratio))
        results.sort(key=lambda x: x[1], reverse=True)
        results_no_ratio = tuple(x[0] for x in results)
        returned_size = min(self.max_pics, len(results_no_ratio))
        return results_no_ratio[:returned_size:]

    def handle_regular_admin_input(self, message, admin_id):
        """
        Executed when there is no delete requests.
        Sent captioned photos are added to collection.
        """
        if message.text is not None and message.text.startswith("/delet"):
            self.bot.send_message(chat_id=message.chat_id,
                                  text="Delete what? Forward a picture.")
            self.deletion_tracker[admin_id] = True
        elif message.photo is not None and message.caption is not None:
            if len(message.photo) == 0:
                self.bot.send_message(chat_id=message.chat_id,
                                      text="Error! Does not compute.")
            pic_id = message.photo[0].file_id
            if message.caption in self.data:
                self.bot.send_message(chat_id=message.chat_id,
                                      text="Error! Duplicate caption.")
            elif pic_id in self.data.values():
                self.bot.send_message(chat_id=message.chat_id,
                                      text="Error! Duplicate image.")
            else:
                self.data[message.caption] = pic_id
                self.bot.send_message(chat_id=message.chat_id,
                                      text="{} -> {}\nOK"
                                      .format(message.caption, pic_id))
                self.dump_data()
        else:
            self.bot.send_message(chat_id=message.chat_id,
                                  text="Sorry, can't understand you.")
        return "OK"

    def handle_deletion_admin_input(self, message, admin_id):
        """
        Executed when there is a delete request.
        Sent photos are deleted from the collection if present.
        """
        if message.photo is not None and len(message.photo) > 0:
            pic_id = message.photo[0].file_id
            if pic_id in tuple(self.data.values()):
                self.data = \
                    {key: value for key, value in self.data.items()
                        if value != pic_id}
                self.bot.send_message(chat_id=message.chat_id,
                                      text="Removal OK.")
                self.dump_data()
            else:
                self.bot.send_message(chat_id=message.chat_id,
                                      text="Error! Image not found.")
        else:
            self.bot.send_message(chat_id=message.chat_id,
                                  text="Error! No image, deletion cancelled.")
        self.deletion_tracker[admin_id] = False
        return "OK"

    def dump_data(self):
        "Saves current collection to file so it can survive restarts."
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent="\t")
