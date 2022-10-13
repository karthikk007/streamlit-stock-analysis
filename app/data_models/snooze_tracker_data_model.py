from .data_model import DataModel
from data_models.ticker_data_model import TickerDataModel


class SnoozeTrackerDataModel(DataModel):
    kduration = '10d'

    def __init__(self, ticker: TickerDataModel) -> None:
        self.duration = self.kduration
        self.ticker = ticker

    @staticmethod
    def from_json(dict):
        duration = dict['duration']
        ticker = TickerDataModel.from_json(dict['ticker'])

        return SnoozeTrackerDataModel(ticker)
