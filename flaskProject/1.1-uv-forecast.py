import tensorflow as tf
import os
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def get_forecasted_uv():
    """
    Call parquet file to forecast hourly UV index for the current day
    :param: None
    :return: JSON file with forecasted UV index
    """
    pass

def reshape_data(data, timesteps=24):
  """
  Reshape data into 3D array for model prediction
  """
  X_reshaped = []
  for i in range(len(data) - timesteps + 1):
    X_reshaped.append(data[i:i + timesteps])
  return np.array(X_reshaped)

def get_features():
    """
    Pre-process features into array X for model prediction
    :param: None
    :return: Numpy array X with features for model prediction
    """
    # Extract current time
    curr_day = dt.datetime.now().day
    curr_month = dt.datetime.now().month
    curr_year = dt.datetime.now().year

    # List of cities to forecast
    cities = ['Adelaide','Brisbane','Canberra','Melbourne','Perth','Sydney']

    # List of hours to forecast
    hours = list(range(0,24))

    # Create empty list to store features
    features = []

    # Loop through each city and hour for features
    for city in cities:
        for hour in hours:
            features.append([city, curr_day, curr_month, curr_year, hour])

    # Create features dataframe
    features_df = pd.DataFrame(features, columns=['city', 'Day', 'Month', 'Year', 'Hour'])

    # One-hot encode city
    # Pre-process city names into dummy binary variables
    processed_data = pd.get_dummies(features_df)
    for city in cities:
        processed_data[f'city_{city}'] = processed_data[f'city_{city}'].astype(int)

    # Normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(processed_data[['Day','Month','Year','Hour']])
    processed_data[['Scaled_Day','Scaled_Month','Scaled_Year','Scaled_Hour']] = pd.DataFrame(scaled_data, columns=['Day','Month','Year','Hour'])

    # Drop the original columns except year
    processed_data = processed_data.drop(columns=['Day','Month','Hour'])