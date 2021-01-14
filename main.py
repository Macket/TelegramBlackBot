import time
import datetime
from timeloop import Timeloop
import handlers
from bots.telegram_bot import telegram_bot
from grid_trading import update_grid


tl = Timeloop()


@tl.job(interval=datetime.timedelta(seconds=5))
def update_grid_job():
    update_grid()


tl.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('stop')
    break

while True:
    try:
        telegram_bot.polling(none_stop=True, interval=1, timeout=0)
    except:
        time.sleep(10)
