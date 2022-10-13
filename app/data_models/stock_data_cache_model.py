import datetime
import json

from .data_model import DataModel


class StockDataCacheModel(DataModel):
    def __init__(self, symbol, start: datetime, end: datetime, path) -> None:
        super().__init__()
        self.symbol = symbol
        self.start = start
        self.end = end
        self.path = path

    @staticmethod
    def from_json(dict):
        symbol = dict['symbol']
        start = dict['start']
        end = dict['end']
        path = dict['path']

        return StockDataCacheModel(symbol, start, end, path)

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, StockDataCacheModel):
            dict = {
                'symbol': o.symbol,
                'start': o.start.isoformat(),
                'end': o.end.isoformat(),
                'path': o.path
            }
            return dict

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, datetime.date):
            return o.isoformat()

        return o.__dict__