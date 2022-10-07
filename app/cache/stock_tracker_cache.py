from cache.cache import Cache

import os
import json

class StockTrackerCache(Cache):
    name = 'stock_tracker_config'
    dir_path = 'app/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('track_list')

    def __init__(self) -> None:
        super().__init__()

    def update_cache(self, track_list):
        self.cache.update(track_list)

    def remove_stocks(self, track_list):
        [self.cache.pop(key) for key in track_list.keys()]
 