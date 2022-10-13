import os
import pandas as pd


class CSVReader(object):
    name = 'CSVReader'
    dir_path = 'app/input_files'
    file_name = '{}.json'.format('CSVReader')


    def __init__(self) -> None:
        self.dataframe = None
        self.load_csv()

    def load_csv(self):
        file_path = self.absolute_file_path()
        self.dataframe = pd.read_csv(file_path)

    def absolute_input_dir(self):
        file_path = '{}'.format(self.dir_path)
        directory = os.path.join(os.getcwd(), file_path) 

        return directory


    def absolute_file_path(self):
        dir = self.absolute_input_dir()
        file = os.path.join(dir, self.file_name)

        return file 