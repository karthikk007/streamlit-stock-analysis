
from data_models.data_model import DataModel


class TickerDataModel(DataModel):
    
    def __init__(self, symbol, name) -> None:
        self.symbol = symbol
        self.name = name

    @staticmethod
    def from_json(dict):
        symbol = dict['symbol']
        name = dict['name']

        return TickerDataModel(symbol, name)