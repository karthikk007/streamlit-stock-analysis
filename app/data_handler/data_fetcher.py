


class DataFetcher(object):

    def __init__(self) -> None:
        self.data_cache = None
        

    def __del__(self):
        print('................................ DataFetcher deleted...')


