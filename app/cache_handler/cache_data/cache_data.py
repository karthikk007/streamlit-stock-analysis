import datetime
import json 

class CacheData(object):
    time_stamp = datetime.datetime.now().date()
    data = {}

    def __init__(self) -> None:
        pass
 

class StockCacheData(CacheData):
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

        return StockCacheData(symbol, start, end, path)



class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, StockCacheData):
            dict = {
                'symbol': o.symbol,
                'start': o.start.isoformat(),
                'end': o.end.isoformat(),
                'path': o.path
            }
            return dict

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

