'''
OOP Assignment before starting work
Late August 2024
'''

import pandas as pd
import os

# Global variables:
repo_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
datetime_dtypes = ["datetime64", "datetime64[ns]", "datetime"]

# Class that loads and processes time series data:
class TimeSeriesDataLoader:

    def __init__(self, name):
        self.path = os.path.join(repo_dir, name)
        self.data = pd.read_csv(self.path)
        self.cols = self.data.columns
        self.col_types = self.data.dtypes
        # Initialize target column:
        self.target_col = None
        if 'date' in self.cols:
            self.date_col = self.data['date']
        else:
            self.date_col = None

    
    def set_date_col(self):

        # Check if a column named 'date' exists:
        if self.date_col is not None:

            # Check if the date column is already a datetime dtype:
            if self.date_col.dtype == "datetime64[ns]":

                # Change nothing:
                return self.date_col

            else:

                # Convert existing column to pandas datetime format:
                self.date_col = pd.to_datetime(self.date_col)
                return self.date_col
        else:

            # Cycle through columns and look for datetime columns:
            for col in self.data.columns:

                # Extract date range if a datetime column is detected:
                if self.data[col].dtype in datetime_dtypes:

                    # Define and return the date range:
                    max_date = self.data[col].max()
                    min_date = self.data[col].min()
                    date_range = f'{min_date} to {max_date}'
                    print(f"{col} has date range: {date_range}")
                
                # Examine "object" dtype columns:
                elif self.data[col].dtype == "object":

                    # Print first value of column and prompt user:
                    user_answer = int(input(f"\nDoes {self.data[col][0]} look like a datetime? Answer 1 for yes, 0 for no: "))

                    if user_answer == 1:

                        # Convert to datetime:
                        self.data[col] = pd.to_datetime(self.data[col])
                        print(f"{col} column converted to datetime and renamed to 'date'. Process Complete.")

                        # Rename the column:
                        self.data = self.data.rename(columns={f"{col}": "date"})
                        break
                    else:
                        print("Continuing search...")
                
                else:
                    print(f"{col} datatype: {self.data[col].dtype}")
        
    
    def slice_df(self):
        
        # NOTE: this is where I left off

        # Need to slice to include only date column and target column:
        return (self.data[[self.date_col]])



### START OF USER-PROGRAM DIALOGUE CODE ###

# Useful dialogue functions:


# Dialogue:
test_class = TimeSeriesDataLoader("daily_log_data.csv")

# Print column names and dtypes:
print(f"\nColumn names available for forecast selection: {test_class.col_types}")

# Prompt user for target variable with error handling:
loop1 = True
while loop1:
    col = input(f"\nEnter target variable for time series forecasting: ")

    if col in test_class.cols:

        if col != "date":

            # CALL A METHOD THAT SLICES THE DATAFRAME
            pass




# Test the class below:

# Create an instance with the misnamed date column:
misnamed_date = TimeSeriesDataLoader("wrong_date_col.csv")
# print(misnamed_date.cols)
misnamed_date.set_date_col()
print()
print(misnamed_date.data)
