
import os
import json


class Cache(object):
    name = 'cache'
    dir_path = 'app/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('cache')

    def __init__(self) -> None:
        self.cache = {}
        self.load_cache()

    def absolute_cache_dir(self):
        file_path = '{}'.format(self.dir_path)
        directory = os.path.join(os.getcwd(), file_path) 

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        return directory


    def absolute_file_path(self):
        dir = self.absolute_cache_dir()
        file = os.path.join(dir, self.file_name)

        return file


    def update_cache(self, dict):
        self.cache = dict
        self.save_cache()


    def save_cache(self):
        print('[-------------------- save_cache', self.name)
        cache_file = self.absolute_file_path()

        self.cache = dict(sorted(self.cache.items()))
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

            print('load_dictionary =========', self.name)

            self.perform_cache_eviction()
        else:
            print('Cache file not found at', cache_file)
            print('Creating one for you')
            with open(cache_file,'a+') as f:
                json.dump(self.cache, f, indent=4)


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


      



