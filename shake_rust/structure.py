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
        self.data = pd.read_csv(os.path.join(repo_dir, name))
