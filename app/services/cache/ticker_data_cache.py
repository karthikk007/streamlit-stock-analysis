from services.cache.cache import Cache
import json


class TickerDataCache(Cache):
    name = 'ticker_data_cache'
    dir_path = 'app/services/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('ticker_list')

    def __init__(self) -> None:
        super().__init__()

    def save_cache(self):
        print('[-------------------- save_cache', self.name)
        cache_file = self.absolute_file_path()

        self.cache = dict(self.cache.items())
        # os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4)
