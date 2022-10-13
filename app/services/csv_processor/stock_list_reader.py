
from .csv_reader import CSVReader

class StockListReader(CSVReader):
    name = 'StockListReader'
    dir_path = 'app/services/input_files/stock_list'
    file_name = '{}.csv'.format('STOCK SCREENING V1 - STOCK LIST')

    def __init__(self) -> None:
        super().__init__()
