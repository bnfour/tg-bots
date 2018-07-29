# main app file, simple bottle app
from bottle import route, run, request, static_file
from bot import BotWrapper

# instance to be used
mybot = BotWrapper()

# 8080 was already taken on my host
PORT = 8081


# returns static page with basic info
@route("/")
def return_index_page():
    return static_file("index.html", root="")


# handles any post request, if url matches bot's token, it's getting called
@route("/<string>", method="POST")
def handle_webhook(string):
    if string == mybot.TOKEN:
        return mybot.web_hook(request.json)
    else:
        return "bad request"


# handles requests to pictures
@route("/i/<path>")
def handle_resource(path):
    return static_file(path, root="images/")


# run() has reasonable defaults
if __name__ == '__main__':
    run(port=PORT)
