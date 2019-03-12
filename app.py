# main app file, simple bottle app
from bottle import route, run, request, static_file
from ladder_bot import LadderBot
from cat_macro_bot import CatMacroBot

# instances to be used
bots = (LadderBot(), CatMacroBot())

# 8080 was already taken on my host
PORT = 8081


# returns static page with basic info
@route("/")
def return_index_page():
    return static_file("index.html", root="")


# handles any post request, if url matches bot's token, it's getting called
@route("/<string>", method="POST")
def handle_webhook(string):
    for bot in bots:
        if bot.is_token(string):
            return bot.handle_update(request.json)
    else:
        return "Bad request :("


# handles requests to pictures
@route("/i/<path>")
def handle_resource(path):
    return static_file(path, root="images/")


# run() has reasonable defaults
if __name__ == '__main__':
    run(port=PORT)
