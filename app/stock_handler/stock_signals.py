
from config.config import Tracker


class StockSignals(object):
    buy_stock_signals = {}
    sell_stock_signals = {}
    tracker = Tracker()

    def __init__(self) -> None:
        self.buy_stock_signals = self.tracker.track_list
        self.sell_stock_signals = self.tracker.track_list

    

    


