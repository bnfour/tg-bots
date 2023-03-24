# main app file, simple bottle app
from bottle import route, run, request, static_file, template, HTTPResponse

from ladder_bot import LadderBot
from cat_macro_bot import CatMacroBot

from bot_info import BotInfo

# instances to be used
bots = (LadderBot(), CatMacroBot())
# their info, and an empty value to generate a placeholder
bots_info: tuple[BotInfo] = tuple([bot.get_data() for bot in bots] + [BotInfo.get_placeholder_info(),])

# 8080 was already taken on my host
PORT = 8081


# returns static page with basic info
@route("/")
def return_index_page() -> HTTPResponse:
    return template("views/index.tpl", data=bots_info)


# handles any post request, if url matches bot's token, it's getting called
@route("/<string>", method="POST")
def handle_webhook(string: str) -> HTTPResponse:
    for bot in bots:
        if bot.is_active() and bot.is_token(string):
            return bot.handle_update(request.json)
    else:
        return HTTPResponse(status=404)


# handles requests to pictures
@route("/i/<path>")
def handle_resource(path: str) -> HTTPResponse:
    return static_file(path, root="images/")


# run() has reasonable defaults for the way i host stuff, ymmv
if __name__ == '__main__':
    run(port=PORT)
