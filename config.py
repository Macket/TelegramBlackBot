import os
from dotenv import load_dotenv

load_dotenv()

# --- TELEGRAM ---
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_ID = int(os.getenv('USER_ID'))

# --- WAVES ---

# [main]
NODE = os.getenv('NODE')
NETWORK = os.getenv('NETWORK')
MATCHER = os.getenv('MATCHER')
ORDER_FEE = int(os.getenv('ORDER_FEE'))
ORDER_LIFETIME = int(os.getenv('ORDER_LIFETIME'))

# [account]
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# [assets]
AMOUNT_ASSET = os.getenv('AMOUNT_ASSET')
PRICE_ASSET = os.getenv('PRICE_ASSET')
