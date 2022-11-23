from data_models.stock_data_cache_model import StockDataCacheModel
from data_models.stock_data_cache_model import Encoder
from services.cache.cache import Cache

import shutil
from datetime import date, datetime, timedelta
import os
import json
import pandas as pd

class StockDataCache(Cache):
    name = 'stock_data_cache'
    dir_path = 'app/services/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('stock_cache')

    def __init__(self) -> None:
        super().__init__()


    def get_file_name(self, symbol, key):
        return '{}.{}.pickle'.format(key, symbol)


    def get_directory_for(self, symbol):
        directory = self.absolute_cache_dir()
        directory = os.path.join(directory, '.stocks')

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        return os.path.join(directory, symbol)


    def get_file_path_for(self, symbol, key):
        directory = self.get_directory_for(symbol)
        file_name = self.get_file_name(symbol, key)
        file = os.path.join(directory, file_name)

        os.mkdir(directory) if not os.path.exists(directory) else None

        return file
            

    def update_cache(self, symbol, key, data, start: datetime, end: datetime):
        print('[-------------------- update_cache')
        path = self.get_file_path_for(symbol, key)

        data.to_pickle(path)

        frame = self.cache.get(symbol)

        cache_data = StockDataCacheModel(symbol, start, end, path)
        cache_data_dict = cache_data.__dict__

        if frame is None:
            frame = {key: cache_data_dict}
        else:
            frame[key] = cache_data_dict

        frame['timestamp'] = datetime.now().isoformat()

        self.cache[symbol] = frame

        self.save_cache()


    def save_cache(self):
        print('[-------------------- save_cache')
        cache_file = self.absolute_file_path()

        self.cache = dict(sorted(self.cache.items()))
        # os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4, cls=Encoder)
            # pickle.dump(self.cache, f)


    def load_cache(self):
        cache_file = self.absolute_file_path()

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.cache = json.load(f)
                # self.cache = pickle.load(f)

            dict = self.cache

            if self.debug:
                print('\n\n')
                print('load_dictionary_index =========', dict.keys())

            self.perform_cache_eviction()
        else:
            print('Cache file not found at', cache_file)


    def perform_cache_eviction(self):

        # print(json.dumps(self.cache, indent=4))

        if len(self.cache):
            eviction_list = []
            file_list = []

            for key, value in self.cache.items():
                stashed_time = value['timestamp']
                timestamp = datetime.fromisoformat(stashed_time)
                
                today = datetime.today()

                print('----------------------')
                print('key = ', key)
                print("stashed_time = ", stashed_time)
                print("today = ", today)

                diff = today - timestamp

                diff_hours = int(diff.seconds / 60 / 60)

                print("diff = ", diff.days)
                print("diff.seconds = ", diff.seconds)
                print("diff_hours = ", diff_hours)

                print(diff_hours)
                if diff_hours >= 6 or diff.days > 1:
                    eviction_list.append(key)
                    for sub_key, sub_value in value.items():
                        if not sub_key == 'timestamp':
                            file_list.append(sub_value['path'])

                print('----------------------\n')

            print('eviction_list = ', eviction_list)

            if len(eviction_list):
                [self.delete_key(x) for x in eviction_list]
                [self.remove_directory(x) for x in file_list]

                self.save_cache()

        if self.debug:
            self.print_cache_stats()


    def delete_key(self, key):
        del self.cache[key]


    def remove_directory(self, path):
        head, tail = os.path.split(path)

        shutil.rmtree(head)

    def print_cache_stats(self):
        ticker_count = 0
        objects_count = 0
        print('\n----------------------------------------')
        print('cache status')
        print('----------------------------------------')
        for key, value in self.cache.items():
            ticker_count = ticker_count + 1
            print('{:>16}\t{:>8}'.format(key, len(value)))
            objects_count = objects_count + len(value)

        print('----------------------------------------')
        print('\tticker = {}\tobjects = {}'.format(ticker_count, objects_count))
        print('----------------------------------------\n')
    

    def get_data(self, path):
        return pd.read_pickle(path)