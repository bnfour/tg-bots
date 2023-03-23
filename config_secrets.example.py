# without the protocol (https://), also keep in mind /{token} will be added to this
SERVER: str = "localhost:8081"

# tokens
LADDER_BOT_TOKEN: str | None = None
CAT_MACRO_BOT_TOKEN: str | None = None

# numeric account ids, not usernames
ADMINS: tuple[int] = tuple() # like (123, 234)
