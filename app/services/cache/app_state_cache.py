from services.cache.cache import Cache


class AppStateCache(Cache):
    name = 'app_state_cache'
    dir_path = 'app/services/cache/.app_state/.{}'.format(name)
    file_name = '{}.json'.format('app_state')

    def __init__(self) -> None:
        super().__init__()