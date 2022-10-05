from cache_handler.cache import Cache

import os
import json

class StockTrackerCache(Cache):
    name = 'stock_tracker_config'
    dir_path = 'app/config/.config_data/.{}'.format(name)
    file_name = '{}.json'.format('track_list')

    def __init__(self) -> None:
        super().__init__()

    def update_cache(self, dict):
        self.cache = dict
        self.save_cache()

    def save_cache(self):
        print('[-------------------- save_cache', self.name)
        cache_file = self.absolute_file_path()

        # os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4)
            # pickle.dump(self.cache, f)


    def load_cache(self):
        print('[-------------------- load_cache', self.name)
        cache_file = self.absolute_file_path()

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.cache = json.load(f)
                # self.cache = pickle.load(f)

            dict = self.cache

            print('load_dictionary =========', self.name)

            self.perform_cache_eviction()
        else:
            print('Cache file not found at', cache_file)

    def perform_cache_eviction(self):
        self.print_cache_stats()

    def print_cache_stats(self):
        ticker_count = 0
        objects_count = 0
        print('\n----------------------------------------')
        print('cache status', self.name)
        print('----------------------------------------')
        for key, value in self.cache.items():
            ticker_count = ticker_count + 1
            # print('{:>16}'.format(key))

        print('----------------------------------------')
        print('\tticker = {}'.format(ticker_count))
        print('----------------------------------------\n')

