from services.cache.cache import Cache


class TickerDataCache(Cache):
    name = 'ticker_data_cache'
    dir_path = 'app/services/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('ticker_list')

    def __init__(self) -> None:
        super().__init__()


