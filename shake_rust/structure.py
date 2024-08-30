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

        if 'date' in self.data.columns:
            self.date_col = self.data['date']
        else:
            self.date_col = None

    # def load_csv(self):
    #     return pd.read_csv(self.path)
    
    def set_date_col(self):
        if self.date_col.dtype != None:

            # Check if the date column is already a datetime dtype:
            if self.date_col.dtype == "datetime64[ns]":

                # Change nothing:
                self.date_col = self.date_col

            else:

                # Convert existing column to pandas datetime format:
                self.date_col = pd.to_datetime(self.date_col)
        else:

            # Cycle through columns and look for datetime columns:
            for col in self.data.columns:

                # Extract date range if a datetime column is detected:
                if self.data[col].dtype == "datetime64[ns]":

                    # Define the date range"
                    max_date = self.data[col].max()
                    min_date = self.data[col].min()
                    date_range = f'{min_date} to {max_date}'

                    # Output col name and range:
                    print(f"{self.data[col].name}: {date_range}")

