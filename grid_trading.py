from bots.black_bot import black_bot
from bots.telegram_bot import telegram_bot
import config
from colors import *


def update_grid():
    # attempt to retrieve order history from matcher
    try:
        history = black_bot.wallet.getOrderHistory(black_bot.asset_pair)
    except:
        history = []

    if history:
        # loop through all grid levels
        # first all ask levels from the lowest ask to the highest -> range(grid.index("") + 1, len(grid))
        # then all bid levels from the highest to the lowest -> range(grid.index("") - 1, -1, -1)
        for n in list(range(0, black_bot.last_level)) + list(range(black_bot.last_level + 1, len(black_bot.grid))):
            # find the order with id == grid9*-+[n] in the history list

            order = [item for item in history if item['id'] == black_bot.grid[n]]
            status = order[0].get("status") if order else ""
            if status == "Filled":
                black_bot.wallet.deleteOrderHistory(black_bot.asset_pair)
                black_bot.grid[n] = ""
                black_bot.last_level = n
                filled_price = float(order[0].get("price")) / 10 ** (black_bot.asset_pair.asset2.decimals + (
                            black_bot.asset_pair.asset2.decimals - black_bot.asset_pair.asset1.decimals))
                filled_type = order[0].get("type")

                black_bot.log("## [%03d] %s%-4s Filled %18.*f%s" % (
                    n, COLOR_BLUE, filled_type.upper(), black_bot.asset_pair.asset2.decimals, filled_price, COLOR_RESET))
                telegram_bot.send_message(
                    config.USER_ID,
                    f'{filled_type.upper()} filled *{filled_price}*',
                    parse_mode='Markdown',
                )

                if filled_type == "buy":
                    black_bot.sell(n + 1)
                    telegram_bot.send_message(
                        config.USER_ID,
                        f'SELL order *{black_bot.get_level_price(n + 1)}*',
                        parse_mode='Markdown',
                    )
                elif filled_type == "sell":
                    black_bot.buy(n - 1)
                    telegram_bot.send_message(
                        config.USER_ID,
                        f'BUY order *{black_bot.get_level_price(n - 1)}*',
                        parse_mode='Markdown',
                    )

            # attempt to place again orders for empty grid levels or cancelled orders
            elif (status == "" or status == "Cancelled") and black_bot.grid[n] != "-":
                black_bot.grid[n] = ""
                if n > black_bot.last_level:
                    black_bot.sell(n)
                elif n < black_bot.last_level:
                    black_bot.buy(n)
