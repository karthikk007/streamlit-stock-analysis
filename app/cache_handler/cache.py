
import os


class Cache(object):
    name = None
    dir_path = 'app/data_source/data_cache'
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

    def load_cache(self):
        assert('Implement in sub class')

    def save_cache(self):
        assert('Implement in sub class')

    def perform_cache_eviction(self):
        assert('Implement in sub class')

    def print_cache_stats(self):
        assert('Implement in sub class')


      



