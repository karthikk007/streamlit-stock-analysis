
from creation_pattern.singletion import SingletonDoubleChecked
from cache.snooze_tracker_cache import SnoozeTrackerCache
from data_models.snooze_tracker_data_model import SnoozeTrackerDataModel

class SnoozeTrackerHandler(SingletonDoubleChecked):

    def __init__(self) -> None:
        super().__init__()
        self.data_cache = SnoozeTrackerCache()

    def get_snooze_list(self):
        snooze_list = {}

        for (key, value) in self.data_cache.cache.items():
            snooze_list[key] = SnoozeTrackerDataModel.from_json(value)

        return snooze_list


    def add_tracker(self, snooze_config_data: SnoozeTrackerDataModel):
        self.data_cache.cache[snooze_config_data.ticker.symbol] = snooze_config_data.__dict__
        self.data_cache.save_cache()

    def remove_tracker(self, snooze_config_data: SnoozeTrackerDataModel):
        self.data_cache.cache.pop(snooze_config_data.ticker.symbol)
        self.data_cache.save_cache()
        


