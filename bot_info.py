from typing import NamedTuple

class BotInfo(NamedTuple):
    """Holds data about a bot to display on the homepage."""
    # bool for true bots, none for the placeholder
    is_online: bool | None
    username: str | None