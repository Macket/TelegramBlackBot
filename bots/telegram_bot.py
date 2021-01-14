import telebot
import config
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

telegram_bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN, threaded=False)
