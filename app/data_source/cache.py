import datetime
from functools import cache
import pandas as pd
import os
import json 

class Cache(object):
    name = None
    cache = {}

    def __init__(self) -> None:
        self.load_cache()

    def cache_dir(self):
        file_path = '{}'.format('app/data_source/data_cache')
        directory = os.path.join(os.getcwd(), file_path) 

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        return directory

    def cache_file_name(self):
        assert('Implement in sub class')

    def cache_file(self):
        dir = self.cache_dir()
        file = os.path.join(dir, self.cache_file_name())

        return file

    def load_cache(self):
        assert('Implement in sub class')

    def save_cache(self):
        assert('Implement in sub class')

    def perform_cache_eviction(self):
        assert('Implement in sub class')

    def print_cache_stats(self):
        assert('Implement in sub class')


class TickerDataCache(Cache):
    name = 'ticker_data_cache'

    def __init__(self) -> None:
        super().__init__()

    def cache_dir(self):
        file_path = '{}'.format('app/data_source/data_cache/.ticker_data')
        directory = os.path.join(os.getcwd(), file_path) 

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        return directory

    def cache_file(self):
        dir = self.cache_dir()
        file = os.path.join(dir, self.cache_file_name())

        return file

    def cache_file_name(self):
        return '{}.json'.format('ticker_list')

    def update_cache(self, dict):
        self.cache = dict
        self.save_cache()

    def save_cache(self):
        print('[-------------------- save_cache', self.name)
        cache_file = self.cache_file()

        os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4)
            # pickle.dump(self.cache, f)


    def load_cache(self):
        print('[-------------------- load_cache', self.name)
        cache_file = self.cache_file()

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

    

class StockDataCache(Cache):
    name = 'stock_data_cache'

    def __init__(self) -> None:
        super().__init__()

    def cache_dir(self):
        file_path = '{}'.format('app/data_source/data_cache/.stock_data')
        directory = os.path.join(os.getcwd(), file_path) 

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        return directory

    def cache_file_name(self):
        return '{}.json'.format('stock_cache')

    def get_key_string(self, start: datetime, end: datetime):
        key = '{}_{}'.format(start.date(), end.date())
        return key

    def get_relative_path(self, symbol):
        return '{}/{}'.format('data_source/data_cache/.stock_data', symbol)

    def get_file_name(self, symbol, key):
        return '{}.{}.pickle'.format(key, symbol)

    def get_directory_for(self, symbol):
        return os.path.join(self.cache_dir(), symbol)

    def get_file_path_for(self, symbol, key):
        directory = self.get_directory_for(symbol)
        file_name = self.get_file_name(symbol, key)
        file = os.path.join(directory, file_name)

        os.mkdir(directory) if not os.path.exists(directory) else None

        return file
        

    def fetch_from_cache(self, symbol, key):

        frame = self.cache.get(symbol)

        if frame is None:
            print('cache miss for', symbol)
            return None

        value = frame.get(key)
        cache_data = None

        if value is not None:
            cache_data = StockCacheData.from_json(value)

        if cache_data is None or not os.path.exists(cache_data.path):
            print('[-------------------- StockDataCache fetch_from_cache ---- cache miss ----')
            return None
        else:
            print('[-------------------- StockDataCache fetch_from_cache ++++ cache hit ++++')
            data = pd.read_pickle(cache_data.path)
            return data
            

    def update_cache(self, symbol, key, data, start: datetime, end: datetime):
        print('[-------------------- update_cache')
        path = self.get_file_path_for(symbol, key)

        data.to_pickle(path)

        frame = self.cache.get(symbol)

        cache_data = StockCacheData(symbol, start, end, path)
        cache_data_dict = cache_data.__dict__

        if frame is None:
            frame = {key: cache_data_dict}
        else:
            frame[key] = cache_data_dict

        self.cache[symbol] = frame

        self.save_cache()


    def save_cache(self):
        print('[-------------------- save_cache')
        cache_file = self.cache_file()

        os.remove(cache_file) if os.path.exists(cache_file) else None

        with open(cache_file, 'w') as f:
            json.dump(self.cache, f, indent=4, cls=Encoder)
            # pickle.dump(self.cache, f)

        print(self.cache.keys())

    def load_cache(self):
        cache_file = self.cache_file()

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.cache = json.load(f)
                # self.cache = pickle.load(f)

            dict = self.cache

            print('load_dictionary_index =========', dict.keys())

            self.perform_cache_eviction()
        else:
            print('Cache file not found at', cache_file)


    def perform_cache_eviction(self):
        self.print_cache_stats()


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
    
      

class CacheData(object):
    time_stamp = datetime.datetime.now().date()
    data = {}

    def __init__(self) -> None:
        pass
 

class StockCacheData(CacheData):
    def __init__(self, symbol, start: datetime, end: datetime, path) -> None:
        super().__init__()
        self.symbol = symbol
        self.start = start
        self.end = end
        self.path = path

    @staticmethod
    def from_json(dict):
        symbol = dict['symbol']
        start = dict['start']
        end = dict['end']
        path = dict['path']

        return StockCacheData(symbol, start, end, path)



class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, StockCacheData):
            dict = {
                'symbol': o.symbol,
                'start': o.start.isoformat(),
                'end': o.end.isoformat(),
                'path': o.path
            }
            return dict

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)




