
import json
from services.csv_processor.stock_list_reader import StockListReader
from services.csv_processor.market_segment_reader import MarketSegmentCategoryReader

def get_market_capital_category():
    reader = MarketSegmentCategoryReader()
    category_df = reader.dataframe

    category_list = category_df["SEGMENT"].to_list()

    return category_list


def get_stock_list():
    reader = StockListReader()

    df = reader.dataframe

    get_ticker_list_for_category()

    return df

def get_ticker_list_for_category(category='CAT-00'):

    reader = StockListReader()

    df = reader.dataframe
    
    dict = df.to_dict('records')

    dict = list(filter(lambda item: item['CATEGORY'] == category, dict))

    return dict