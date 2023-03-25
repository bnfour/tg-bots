# main app file, simple bottle app
from bottle import route, run, request, static_file, template, HTTPResponse
from bots.bot_manager import BotManager

manager = BotManager()
# 8080 was already taken on my host
PORT = 8081


# returns static page with basic info
@route("/")
def return_index_page() -> HTTPResponse:
    return template("views/index.tpl", data=manager.get_info())


# handles any post request, if url matches bot's token, it's getting called
@route("/<string>", method="POST")
def handle_webhook(string: str) -> HTTPResponse:
    return manager.handle_request(string, request.json)


# handles requests to pictures
@route("/i/<path>")
def handle_resource(path: str) -> HTTPResponse:
    return static_file(path, root="images/")


# run() has reasonable defaults for the way i host stuff, ymmv
if __name__ == '__main__':
    run(port=PORT)
