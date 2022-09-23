import json
import os

class BuyTracker(object):
    track_list = {}

    def __init__(self) -> None:
        self.load_list()


    def load_list(self):
        file_path = BuyTracker.file_path()
        print('file_path = ', file_path)

        with open(file_path, 'r') as f:
            self.track_list = json.load(f)

        print(type(self.track_list))
        print(self.track_list)


    def save_list(self):
        file_path = BuyTracker.file_path()
        print('file_path = ', file_path)

        with open(file_path, 'w') as f:
            self.track_list = dict(sorted(self.track_list.items()))
            json.dump(self.track_list, f, indent=4)


    def add_stocks(self, stock_list):
        self.track_list.update(stock_list)


    @staticmethod
    def file_path():
        file = '{}'.format('app/config/track_list.json')
        file_path = os.path.join(os.getcwd(), file) 

        return file_path


