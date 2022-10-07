from cache.cache import Cache


class SnoozeTrackerCache(Cache):
    name = 'snooze_tracker_config'
    dir_path = 'app/cache/.data_cache/.{}'.format(name)
    file_name = '{}.json'.format('snooze_list')

    def __init__(self) -> None:
        super().__init__()

