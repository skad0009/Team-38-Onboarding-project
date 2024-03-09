import os
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
import json

def forecast_uv(debug = False):
    """
    Call parquet file to forecast hourly UV index for the current day
    :param: debug: boolean to write forecast to file
    :return: JSON of forecasted UV-index in the format of {city: city_name, hour: hour, uvIndex: uv_index}
    """
    # Get both processed and raw features
    X, features = get_features()

    # Load model
    model = tf.keras.models.load_model('database/1.1/uv-predict.keras')

    # Make predictions
    y_pred = model.predict(X)

    # Format predictions into JSON
    forecast = process_JSON(features, y_pred)

    ## debugging: write forecast to file
    if debug:
        with open('forecast.json', 'w') as f:
            json.dump(forecast, f)

    return forecast


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
    :return X: Numpy array X with features for model prediction
    :return features_df: Dataframe of features - to be processed into JSON
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

    # Reshape data
    X = reshape_data(processed_data.values)

    return X, features_df

def process_JSON(features, y_pred):
    """
    Process features and predictions into JSON
    :param features: Dataframe of features
    :param y_pred: Numpy array of predictions
    :return: JSON of forecasted UV-index in the format of {city: city_name, hour: hour, uvIndex: uv_index}
    """
    # Create empty list to store JSON
    forecast = []

    # Loop through each city and hour for predictions
    for i in range(len(features)):
        city = features['city'][i]
        hour = features['Hour'][i]
        uvIndex = y_pred[i][0]
        forecast.append({'city': city, 'hour': hour, 'uvIndex': uvIndex})

    return forecast

if __name__ == '__main__':
    forecast_uv()