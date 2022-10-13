from data_models.ticker_data_model import TickerDataModel
from services.cache_handler.ticker_data_handler import TickerDataHandler

ticker_handler = TickerDataHandler.instance()


def ticker_model_from_list(ticker_list):

    models = list(map(lambda ticker: ticker_handler.get_ticker_model(ticker), ticker_list))

    return models