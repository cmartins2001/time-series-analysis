'''
OOP Assignment before starting work
Late August 2024
'''

# Import modules:
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
# Set graphic style:
plt.style.use('fivethirtyeight')

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
        # Initialize target column name and the column itself:
        self.target_col_nm = None
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
                    user_answer = int(input(f"\nDoes {self.data[col][0]} look like a datetime? Answer 1 for YES, 0 for NO: "))

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
        
    
    def slice_df(self, target_col):

        # Set the target column name:
        self.target_col_nm = target_col
        
        # Set the target column to the user input:
        self.target_col = self.data[target_col]

        # Need to slice to include only date column and target column:
        return (self.data[['date', f'{target_col}']])
    

    def target_col_histogram(self):

        # Plot a histogram of the target column:
        plt.figure(figsize=(6, 7))
        sns.histplot(data=self.data, x=self.target_col_nm, kde=True, color='darkviolet')
        plt.title(f'{self.target_col_nm} - Histogram')
        plt.xlabel(self.target_col_nm)
        plt.show()


### START OF USER-PROGRAM DIALOGUE CODE ###

# Useful dialogue functions:


# Creating the class instance:
data_path = str(input("\nPaste the file path of the data to be forecasted, including the '.csv' file extension:\n"))

test_class = TimeSeriesDataLoader(data_path)
raw_df = test_class.data

# Run date column check:
user_select = int(input("Does this file contain a datetime column named 'date'? Answer 0 for NO, 1 for YES, and 2 for NOT SURE: "))

# Answer logic:
loop1 = True
while loop1:
    if user_select in [0, 2]:
        test_class.set_date_col()
        loop1 = False
    elif user_select == 1:
        test_class = test_class
        loop1 = False
    else:
        user_select = int(input("Does this file contain a datetime column named 'date'? Answer 0 for NO, 1 for YES, and 2 for NOT SURE: "))


# Print column names and dtypes:
print(f"\nColumn names available for forecast selection:\n {test_class.col_types}")

# Prompt user for target variable with error handling:
loop2 = True
while loop2:
    col = input(f"\nEnter target variable for time series forecasting: ")

    if col in test_class.cols:

        if col != "date":

            # Call the DF slicing method:
            sliced_df = test_class.slice_df(target_col=col)

            # Show output:
            print(f"\nSliced Dataframe, first 5 rows:\n{sliced_df.head()}")

            # End loop:
            loop2 = False

    else:
        # Re-prompt for target variable:
        col = input(f'\n{col} is not recognized as a column available for selection, please try again: ')

# Prompt user about seeing the distribution of the target variable:
loop3 = True
while loop3:
    user_bool = int(input(f"\nEnter 1 to see the distribution of the {col} colmumn OR enter 0 to SKIP: "))
    if user_bool == 1:
        test_class.target_col_histogram()
        loop3 = False
    elif user_bool == 0:
        loop3 = False

