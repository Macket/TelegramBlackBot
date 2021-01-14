import re
from bots.telegram_bot import telegram_bot
from keyboards import *


def start_set_grid_scenario(message):
    telegram_bot.send_message(message.chat.id, "Hi, Boss! Let's trade!")
    base_price_request(message)


def base_price_request(message):
    telegram_bot.send_message(message.chat.id, 'Set base price', reply_markup=base_price_keyboard())
    telegram_bot.register_next_step_handler(message, base_price_receive)


def base_price_receive(message):
    if message.text == 'Manually':
        manual_base_price_request(message)
    else:
        black_bot.base_price = int(message.text.split(' ')[1])
        interval_request(message)


def manual_base_price_request(message):
    telegram_bot.send_message(
        message.chat.id,
        'Send base price in *nnnnn* format',
        reply_markup=remove_keyboard(),
        parse_mode='Markdown'
    )
    telegram_bot.register_next_step_handler(message, manual_base_price_receive)


def manual_base_price_receive(message):
    if re.search("^[0-9]{5}$", message.text):
        black_bot.base_price = int(message.text)
        interval_request(message)
    else:
        telegram_bot.send_message(message.chat.id, 'Wrong format. Try again with *nnnnn* format', parse_mode='Markdown')
        telegram_bot.register_next_step_handler(message, manual_base_price_receive)


def interval_request(message):
    telegram_bot.send_message(
        message.chat.id,
        'Set step interval in percents, for example *3* or *12*',
        reply_markup=remove_keyboard(),
        parse_mode='Markdown')
    telegram_bot.register_next_step_handler(message, interval_receive)


def interval_receive(message):
    if re.search("^[0-9]{1,2}$", message.text):
        black_bot.interval = int(message.text) / 100
        grid_levels_request(message)
    else:
        telegram_bot.send_message(message.chat.id, 'Wrong format. Try again', parse_mode='Markdown')
        telegram_bot.register_next_step_handler(message, interval_receive)


def grid_levels_request(message):
    telegram_bot.send_message(
        message.chat.id,
        'Set number of bid and ask orders. Send them in format *N N*, for example *3 12*',
        parse_mode='Markdown'
    )
    telegram_bot.register_next_step_handler(message, grid_levels_receive)


def grid_levels_receive(message):
    try:
        [bid_levels, ask_levels] = map(lambda x: int(x), message.text.split(' '))
        black_bot.grid_levels = bid_levels + 1 + ask_levels
        black_bot.base_level = bid_levels
        black_bot.last_level = black_bot.base_level
        black_bot.grid = ["-"] * black_bot.grid_levels
        tranche_size_request(message)
    except:
        telegram_bot.send_message(message.chat.id, 'Wrong format. Try again', parse_mode='Markdown')
        telegram_bot.register_next_step_handler(message, grid_levels_receive)


def tranche_size_request(message):
    telegram_bot.send_message(
        message.chat.id,
        'Set tranche size in WAVES, for example *10.5*',
        parse_mode='Markdown',
    )
    telegram_bot.register_next_step_handler(message, tranche_size_receive)


def tranche_size_receive(message):
    try:
        black_bot.tranche_size = int(float(message.text) * 10 ** black_bot.asset_pair.asset1.decimals)
        telegram_bot.send_message(
            message.chat.id,
            f'Here is your grid parameters:\n\n'
            f'Base price: *{black_bot.base_price}*\n'
            f'Interval: *{black_bot.interval}*\n'
            f'Bids: *{black_bot.base_level}*\n'
            f'Asks: *{black_bot.grid_levels - 1 - black_bot.base_level}*\n'
            f'Tranche size: *{black_bot.tranche_size}*',
            reply_markup=set_grid_keyboard(),
            parse_mode='Markdown',
        )
        telegram_bot.register_next_step_handler(message, set_grid)
    except:
        telegram_bot.send_message(message.chat.id, 'Wrong format. Try again', parse_mode='Markdown')
        telegram_bot.register_next_step_handler(message, tranche_size_receive)


def set_grid(message):
    telegram_bot.send_message(message.chat.id, 'Grid setting...', reply_markup=remove_keyboard())

    [bids, asks] = black_bot.init_grid()

    msg_text = ''
    for bid in bids:
        msg_text += f'BID {black_bot.tranche_size} *{bid}*\n'
    msg_text += '\n'
    for ask in asks:
        msg_text += f'ASK {black_bot.tranche_size} *{ask}*\n'
    telegram_bot.send_message(message.chat.id, msg_text, parse_mode='Markdown')
