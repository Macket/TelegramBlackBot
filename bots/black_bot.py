import pywaves as pw
import datetime
import config
from colors import *


class BlackBot:
    def __init__(self):
        # main
        self.node = config.NODE
        self.chain = config.NETWORK
        self.matcher = config.MATCHER
        self.order_fee = config.ORDER_FEE
        self.order_lifetime = config.ORDER_LIFETIME

        # account
        self.private_key = config.PRIVATE_KEY
        self.wallet = pw.Address(privateKey=self.private_key)

        # assets
        self.amount_asset_id = config.AMOUNT_ASSET
        self.price_asset_id = config.PRICE_ASSET
        self.asset_pair = pw.AssetPair(pw.Asset(self.amount_asset_id), pw.Asset(self.price_asset_id))

        # grid
        self.base_price = 0
        self.interval = 0.01
        self.grid_levels = 20
        self.base_level = 10
        self.last_level = 10
        self.grid = ["-"] * self.grid_levels
        self.tranche_size = 150000000  # 1.5 WAVES

    def log(self, msg):
        timestamp = datetime.datetime.utcnow().strftime("%b %d %Y %H:%M:%S UTC")
        s = "[%s] %s:%s %s" % (timestamp, COLOR_WHITE, COLOR_RESET, msg)
        print(s)

    def get_last_price(self):
        try:
            last_trade_price = int(float(self.asset_pair.last()) * 10 ** (
                    self.asset_pair.asset2.decimals + (
                        self.asset_pair.asset2.decimals - self.asset_pair.asset1.decimals)))
        except:
            last_trade_price = 0
        return last_trade_price

    def get_level_price(self, level):
        price = int(self.base_price * (1 + self.interval) ** (level - self.base_level))
        price = int(price / 100) * 100
        price = round(price / 10 ** (self.asset_pair.asset2.decimals +
                                     (self.asset_pair.asset2.decimals - self.asset_pair.asset1.decimals)), 8)
        price = float(str(price))

        return price

    def init_grid(self):
        self.log("Grid initialisation [base price : %.*f]" % (
            self.asset_pair.asset2.decimals, float(self.base_price) / 10 ** self.asset_pair.asset2.decimals))
        self.log("Grid initialisation [base price : %.*f]" % (
            self.asset_pair.asset2.decimals,
            float(self.base_price) / 10 ** (self.asset_pair.asset2.decimals +
                                            (self.asset_pair.asset2.decimals - self.asset_pair.asset1.decimals))))

        pw.setNode(node=self.node, chain=self.chain)
        pw.setMatcher(node=self.matcher)
        self.log("Cancelling open orders...")
        self.wallet.cancelOpenOrders(self.asset_pair)  # cancel all open orders on the specified pair

        self.log("Deleting order history...")
        self.wallet.deleteOrderHistory(self.asset_pair)  # delete order history on the specified pair

        bids = []
        for n in range(0, self.base_level):
            self.buy(n)
            bids.append(self.get_level_price(n))

        asks = []
        for n in range(self.base_level + 1, self.grid_levels):
            self.sell(n)
            asks.append(self.get_level_price(n))

        return bids, asks

    def buy(self, level):
        if 0 <= level < self.grid_levels and (self.grid[level] == "" or self.grid[level] == "-"):
            try:
                order = self.wallet.buy(self.asset_pair, self.tranche_size, self.get_level_price(level),
                                        matcherFee=self.order_fee, maxLifetime=self.order_lifetime)
                order_id = order.orderId
                self.log(">> [%03d] %s%-4s order  %18.*f%s" % (
                    level, COLOR_GREEN, 'BUY', self.asset_pair.asset2.decimals, self.get_level_price(level), COLOR_RESET))
            except:
                order_id = ""
            self.grid[level] = order_id

    def sell(self, level):
        if 0 <= level < self.grid_levels and (self.grid[level] == "" or self.grid[level] == "-"):
            try:
                order = self.wallet.sell(self.asset_pair, self.tranche_size, self.get_level_price(level),
                                         maxLifetime=self.order_lifetime, matcherFee=self.order_fee)
                order_id = order.orderId
                self.log(">> [%03d] %s%-4s order  %18.*f%s" % (
                    level, COLOR_RED, 'SELL', self.asset_pair.asset2.decimals, self.get_level_price(level), COLOR_RESET))
            except:
                order_id = ""
            self.grid[level] = order_id


black_bot = BlackBot()
