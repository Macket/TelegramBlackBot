from telebot import types
from bots.black_bot import black_bot


def remove_keyboard():
    return types.ReplyKeyboardRemove()


def base_price_keyboard():
    last_price = black_bot.get_last_price()
    bid_price = black_bot.asset_pair.orderbook()['bids'][0]['price']
    ask_price = black_bot.asset_pair.orderbook()['asks'][0]['price']

    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(
        types.KeyboardButton(f'ASK {ask_price}'),
        types.KeyboardButton(f'LAST {last_price}'),
        types.KeyboardButton(f'BID {bid_price}'),
        types.KeyboardButton('Manually'),
    )

    return keyboard


def set_grid_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(types.KeyboardButton('Set grid'))
    return keyboard
