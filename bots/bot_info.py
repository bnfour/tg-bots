from typing import NamedTuple

class BotInfo(NamedTuple):
    """Holds data about a bot to display on the homepage."""
    # bool for true bots, none for the placeholder
    is_online: bool | None
    username: str | None

    @staticmethod
    def get_placeholder_info():
        """
        Returns a special data entry that does not correspond to a bot.
        Instead, it is used for a placeholder.
        """
        # setting is_online to None marks it as a placholder
        return BotInfo(None, None)
