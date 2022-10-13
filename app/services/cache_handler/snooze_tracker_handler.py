
from datetime import datetime, date
from helpers.dictionary_helpers import todict
from data_models.stock_data_cache_model import Encoder
from helpers.ticker_helper import ticker_model_from_list
from creation_pattern.singletion import SingletonDoubleChecked
from services.cache.snooze_tracker_cache import SnoozeTrackerCache
from data_models.snooze_tracker_data_model import SnoozeTrackerDataModel

import json

class SnoozeTrackerHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = SnoozeTrackerCache()

    def get_snooze_list(self):
        snooze_list = {}

        self.data_cache.perform_cache_eviction()

        for (key, value) in self.data_cache.cache.items():
            snooze_list[key] = SnoozeTrackerDataModel.from_json(value)

        return snooze_list


    def add_tracker(self, snooze_config_data: SnoozeTrackerDataModel):
        print(snooze_config_data.ticker.symbol)
        if self.data_cache.cache.get(snooze_config_data.ticker.symbol, None) is None:
            self.data_cache.cache[snooze_config_data.ticker.symbol] = json.dumps(self.cache, indent=4, cls=Encoder) #snooze_config_data.__dict__
            self.data_cache.save_cache()

    def remove_tracker(self, snooze_config_data: SnoozeTrackerDataModel):
        self.data_cache.cache.pop(snooze_config_data.ticker.symbol)
        self.data_cache.save_cache()

    def has_key(self, symbol):
        if symbol in self.data_cache.cache:
            return True

        return False

    def snooze_list(self, snooze_list):
        models = ticker_model_from_list(snooze_list)

        print(snooze_list)

        for model in models:
            if not self.has_key(model.symbol):
                snooze_model = SnoozeTrackerDataModel(model)
                value_dict = todict(snooze_model)
                value_dict['timestamp'] = datetime.now().date().isoformat()
                dict = {model.symbol: value_dict}
                self.data_cache.append_data(dict)
            else:
                print('snooze_list - Key exists already: ', model.symbol)
        
        self.data_cache.save_cache()
        


