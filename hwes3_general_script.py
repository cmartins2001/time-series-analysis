'''
Estimating a Holt-Winters Exponential Smoothing Model with Python
By Connor Martins
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.graphics.tsaplots import plot_acf
import sklearn
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
plt.style.use('fivethirtyeight')


# Function that reads data into a pandas DF based on a user-specified file name:
def read_data(file_name, df_index, ts_var):
    path = os.path.join('c:' + os.sep, 'Users', 'cmart', 'PycharmProjects', 'streamlit_stuff', 'time series', 'seoul_forecasting', file_name)                 # Alter the start of the folder path as needed
    df = pd.read_csv(path, encoding='ISO-8859-1', parse_dates=['Date'], dayfirst=True)  # Only parse dates if needed
    main_df = df.loc[:, (df_index, ts_var)]         # Creates a time series dataframe with index and series only
    main_df.set_index(df_index, inplace=True)       # Sets index to desired variable (usually a date/datetime)
    """
    Use these lines for further data cleansing (such as aggregation using groupby, etc.)
    """
    return main_df                                  # This function returns the dataset cleaned for TSA


# Function that generates a time series plot using matplotlib:
def ts_plot(dataframe, index, yt):
    plt.figure(figsize=(9,5))
    plt.plot(dataframe.index, dataframe[yt], color='lightblue')     # Where yt is the time series
    plt.title(f'{yt} Over Time')
    plt.xlabel(f'{index}')
    plt.ylabel(f'{yt}')
    max_ticks = 10                                                  # Adjust to data size/range
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=max_ticks))
    plt.show()


# Function that seasonally decomposes the time series using statsmodel library:
def decompose(dataframe, index, yt, model_type, period):
    decomp = seasonal_decompose(dataframe[yt], model=model_type, period=period)     # Need to decide periods and add/mult
    decomp.plot()
    return decomp.seasonal


# Function that plots the ACF of the time series seasonal component to determine seasonal periods:
def seasonal_acf(seasonal_component, lags, yt):
    plot_acf(seasonal_component, lags=lags)
    plt.show()


# Assuming that the time series exhibits seasonality and trend, and has only values > 0, move to test/train split:
def data_split(dataframe, prediction_period):
    train_data = dataframe[:-prediction_period]     # Typically set the prediction period to data frequency (e.g., 1 week)
    test_data = dataframe[-prediction_period:]
    return train_data, test_data


# Fit the initial triple exponential smoothing model on the training data and generate initial predictions:
def model_fit(train, yt, prediction_period, seasonal_type, seasonal_periods,trend_type, data_freq):
    HWES3_model = ExponentialSmoothing(train[yt], trend=trend_type, seasonal=seasonal_type, seasonal_periods=seasonal_periods, freq=data_freq).fit()        # Adjust model types and freq according to data
    HWES3_fitted = HWES3_model.fittedvalues
    HWES3_predictions = HWES3_model.forecast(prediction_period)         # Use the same prediction period as in data split
    return HWES3_fitted, HWES3_predictions


# Plot the training data, test data, and model predictions together:
def plot_initial(train, yt, predictions, index, test):
    plt.figure(figsize=(15, 6))
    plt.plot(train.index, train[yt], label='Training Data', color='lightblue')
    plt.plot(test[yt], label='Test Data', color='seagreen')             # Use second value from data_split
    plt.plot(predictions, label='HWES3 Predictions', color='red')       # Use second value from model_fit
    plt.xlabel(f'{index}')
    plt.ylabel(f'{yt}')
    plt.title('HWES3 Predictions vs. Test Data')
    plt.legend()
    plt.grid(True)
    max_ticks = 10      # Adjust as needed
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=max_ticks))
    plt.show()


# Fit the final model on the full dataset:
def fit_final_mdoel(dataframe, yt, prediction_period, seasonal_type, seasonal_periods,trend_type, data_freq):
    HWES3_final_model = ExponentialSmoothing(dataframe[yt], trend=trend_type, seasonal=seasonal_type, seasonal_periods=seasonal_periods, freq=data_freq).fit()
    HWES3_final_fitted = HWES3_final_model.fittedvalues
    HWES3_forecast = HWES3_final_model.forecast(prediction_period)
    return HWES3_final_fitted, HWES3_forecast


# Pot full dataset with final forecast:
def plot_final(dataframe, yt, forecast, index):
    plt.figure(figsize=(12, 6))
    plt.plot(dataframe.index, dataframe[yt], label='Actual Data', color='lightblue')
    plt.plot(forecast, label='HWES3 Forecast', color='red', linestyle='--')
    plt.xlabel(f'{index}')
    plt.ylabel(f'{yt}')
    plt.title('HWES3 Forecast vs. Actual Data')
    plt.legend()
    plt.grid(True)
    max_ticks = 10      # Adjust as needed
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=max_ticks))
    plt.show()


# Call all of the functions here:
def main():
    # Create a DF:
    ts_df = read_data('SeoulBikeData.csv', df_index='Date', ts_var='Rented Bike Count')
    # Plot the time series:
    """ts_plot(ts_df, 'Date', 'Rented Bike Count')
    # Seasonally decompose it:
    seasonal_comp = decompose(ts_df, index='Date', yt='Rented Bike Count', model_type='additive', period=24)
    # Plot seasonality ACF:
    seasonal_acf(seasonal_component=seasonal_comp, lags=100, yt='Rented Bike Count')"""
    # Split the data into training and test:
    new_dfs = data_split(dataframe=ts_df, prediction_period=7)    # Forecast to data period (7 days in this case)
    train_data = new_dfs[0]
    test_data = new_dfs[1]
    # Fit the HWES3 model:
    model = model_fit(train=train_data, yt='Rented Bike Count', seasonal_type='add', seasonal_periods=7, trend_type='add', data_freq='D', prediction_period=7)
    predictions1 = model[1]
    # Plot the initial model versus the test:
    plot_initial(train=train_data, yt='Rented Bike Count', index='Date', test=test_data)    # I did not agg the data by day so i need to change the frequency argument to make it make sense



if __name__ == '__main__':
    main()
