import functools
import config
from bots.telegram_bot import telegram_bot


def user_checker(func):
    @functools.wraps(func)
    def check_user(message):
        if message.chat.id == config.USER_ID:
            func(message)
        else:
            telegram_bot.send_message(message.chat.id, 'You are not my Boss! Get out!')
    return check_user
