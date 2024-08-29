'''
OOP Assignment before starting work
Late August 2024
'''

import pandas as pd
import os

# Global variables:
repo_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script

# Class that loads and processes time series data:
class TimeSeriesDataLoader:

    def __init__(self, name):
        self.path = os.path.join(repo_dir, name)
        self.data = pd.read_csv(self.path)
        self.date_col = self.data['date']

    # def load_csv(self):
    #     return pd.read_csv(self.path)
    
    def set_date_col(self):
        if self.date_col.dtype != None:
            if self.date_col.dtype == "datetime64":
                print("Date column is already in datetime format.")
            else:
                self.date_col = pd.to_datetime(self.date_col)
                print("Date column was SET to datetime format.")
        else:
            print("There is no column named 'date', please check source data and try again.")

