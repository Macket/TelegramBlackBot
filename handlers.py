from bots.telegram_bot import telegram_bot
from decorators import user_checker
from scenarios.set_grid_scenario import start_set_grid_scenario


@telegram_bot.message_handler(commands=['start'])
@user_checker
def start(message):
    start_set_grid_scenario(message)
