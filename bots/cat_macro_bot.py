import json
import telegram
import os

from fuzzywuzzy import fuzz
from bottle import HTTPResponse
from typing import List, Tuple, Dict, Iterable

from .bot_base import BotBase


class CatMacroBot(BotBase):
    "Class for inline searches of predefined collection of pictures"
    inline_purpose = "matching cat pictures"
    # path to physical backup of available pictures
    file_path = "data/cat_pics.json"
    # up to this amount of somewhat relevant pics will be served
    max_pics = 7
    # ratio of similarity threshold between image captions and provided query
    similarity_threshold = 50

    def __init__(self, server: str, token: str | None, admins: Iterable[int]):
        super().__init__(server, token, admins)
        # loading of exisiting data
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.data: Dict[str, str] = json.load(file)
        else:
            self.data: Dict[str, str] = dict()

    def handle_message(self, message: telegram.Message) -> HTTPResponse:
        "Responds to /start, also adds pictures from admins to collection."
        if message.text is not None and message.text == "/start":
            self.send_inline_start(message)
        elif self.is_message_from_admin(message):
            return self.handle_admin_input(message)
        else:
            self.send_inline_nag(message)

        return HTTPResponse(body="OK", status=200)

    def handle_inline_query(self, inline_query: telegram.InlineQuery) -> HTTPResponse:
        "Returns inline results."
        results = self.generate_inline_results(inline_query.query)
        self.bot.answer_inline_query(inline_query.id, results)

        return HTTPResponse(body="OK", status=200)

    def generate_inline_results(self, query: str) -> List[telegram.InlineQueryResultCachedPhoto]:
        "Generates inline answers as pictures already saved as Telegram media."
        inline_results = []
        for ans_id, media_id in enumerate(self.find_most_relevant_pics(query)):
            r = telegram.InlineQueryResultCachedPhoto(ans_id, media_id)
            inline_results.append(r)
        return inline_results

    def find_most_relevant_pics(self, query: str) -> Tuple[str]:
        "Finds up to max_pics results and returns them as tuple of media ids"
        # skip too short queries
        if len(query) < 3:
            return tuple()
        # populate a list of (ratio, media id) for entries
        # with somewhat matching ratios
        results: List[Tuple[str, int]] = []
        for caption in self.data:
            ratio = fuzz.partial_ratio(query, caption)
            if ratio > self.similarity_threshold:
                results.append((self.data[caption], ratio))
        # take up to max_pics best matching results
        entries_to_take = min(self.max_pics, len(results))
        results.sort(key=lambda x: x[1], reverse=True)
        return tuple(x[0] for x in results[:entries_to_take])

    def handle_admin_input(self, message: telegram.Message) -> HTTPResponse:
        """
        Executed when there is no delete requests.
        Sent captioned photos are added to collection.
        """
        if message.text is not None:
            text = message.text.split(" ", maxsplit=1)
            command = text[0]
            if command.startswith("/delet") and len(text) > 1:
                caption = text[1]
                if len(self.data) > 0 and caption in self.data:
                    del self.data[caption]
                    self.dump_data()
                    self.reply(message, "Removal OK")
                else:
                    self.reply(message, f"Error! Nothing to delete for \"{caption}\"")
            else:
                self.reply(message, "Sorry, can't understand you.")
        elif message.photo is not None and message.caption is not None:
            if len(message.photo) > 0:
                pic_id = message.photo[0].file_id
                if message.caption in self.data:
                    self.reply(message, "Error! Duplicate caption.")
                # TODO there was a check for the same image, but it did't work,
                # because file_id we used to check is not the same (file_unique_id is)
                # for the reuploads of the same image
                # but to think, why would we limit this anyway?
                else:
                    self.data[message.caption] = pic_id
                    self.dump_data()
                    self.reply(message, f"{message.caption} → {pic_id}\nOK")
            else:
                self.reply(message, "Error! Does not compute.")
        else:
            self.reply(message, "Sorry, can't understand you.")

        return HTTPResponse(body="OK", status=200)

    def dump_data(self) -> None:
        "Saves current collection to file so it can survive restarts."
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent="\t")
