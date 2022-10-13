
from time import time
from data_models.stock_data_cache_model import Encoder
from services.cache.cache import Cache

from datetime import date, datetime, timedelta
import json


class SnoozeTrackerCache(Cache):
    name = 'snooze_tracker_cache'
    dir_path = 'app/services/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('snooze_list')

    def __init__(self) -> None:
        super().__init__()


    def append_data(self, dict):
        self.cache.update(dict)

    def save_cache(self):
        print('[-------------------- save_cache', self.name)
        cache_file = self.absolute_file_path()

        self.cache = dict(sorted(self.cache.items()))
        # os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4, cls=Encoder)
            # pickle.dump(self.cache, f)


    def perform_cache_eviction(self):
        self.print_cache_stats()

        if len(self.cache):
            eviction_list = []

            for (key, value) in self.cache.items():
                duration = value['duration']
                timestamp = value['timestamp']

                days = ''.join(filter(lambda i: i.isdigit(), duration))

                timestamp = datetime.fromisoformat(timestamp)
                timestamp = timestamp + timedelta(days=int(days))
                
                today = datetime.today()

                diff = today - timestamp

                if diff.days >= 0:
                    eviction_list.append(key)

            if len(eviction_list):
                [self.delete_key(x) for x in eviction_list]

                self.save_cache()


    def delete_key(self, key):
        del self.cache[key]

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