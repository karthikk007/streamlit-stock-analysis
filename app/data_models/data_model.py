import datetime
import json 


class DataModel(object):
    time_stamp = datetime.datetime.now().date()
    data = {}

    def __init__(self) -> None:
        pass
