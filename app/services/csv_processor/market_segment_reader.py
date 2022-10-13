
from .csv_reader import CSVReader

class MarketSegmentCategoryReader(CSVReader):
    name = 'MarketSegmentCategoryReader'
    dir_path = 'app/services/input_files/market_category'
    file_name = '{}.csv'.format('Constants - MARKET SEGMENT')

    def __init__(self) -> None:
        super().__init__()