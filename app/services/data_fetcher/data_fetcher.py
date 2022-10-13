


class DataFetcher(object):

    def __init__(self) -> None:
        self.cache_handler = None

    def __del__(self):
        print('................................ DataFetcher deleted...')


