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
    Call keras file to forecast hourly UV index for the current day
    :param: debug: boolean to write forecast to file
    :return: JSON of forecasted UV-index in the format of {city: city_name, hour: hour, uvIndex: uv_index}
    """
    # Get both processed and raw features
    X, features = get_features()

    # Load model
    model = tf.keras.models.load_model('database/1.1/uv-predict.h5')

    # Make predictions
    y_pred = model.predict(X)

    # Adjust predictions to be between 0 and 11
    y_pred = np.round(y_pred, 0)
    y_pred = np.clip(y_pred, 0, 11)

    # Format predictions into JSON
    forecast = process_JSON(features, y_pred)

    ## debugging: write forecast to file
    if debug:
        with open('test/forecast.json', 'w') as f:
            json.dump(forecast, f)

    return forecast

def reshape_data(data, timesteps=24):
    """
    Reshape data into 3D array for model prediction
    :param data: Numpy array of features
    :param timesteps: Number of timesteps to consider
    :return: Numpy array of reshaped features
    """
    data_length = len(data)
    X_reshaped = []

    for i in range(data_length):
        # If remaining data is less than timesteps, pad with zeros
        if i + timesteps > data_length:
            remaining_data = data[i:]
            padding = np.zeros((timesteps - len(remaining_data), data.shape[1]))
            X_reshaped.append(np.concatenate([remaining_data, padding]))
        else:
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

    # print(f"Size of processed data: {processed_data.shape}")

    # Normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(processed_data[['Day','Month','Year','Hour']])
    processed_data[['Scaled_Day','Scaled_Month','Scaled_Year','Scaled_Hour']] = pd.DataFrame(scaled_data, columns=['Day','Month','Year','Hour'])

    # print(f"Size of scaled data: {processed_data.shape}")

    # Drop the original columns except year
    processed_data = processed_data.drop(columns=['Day','Month','Hour','Year'])

    # print(f"Size of data after dropping columns: {processed_data.shape}")

    # Reshape data
    X = reshape_data(processed_data.values)

    # print(f"Size of reshaped data: {X.shape}")

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

    # print(f"Features: {features.shape}")
    # print(f"y_pred: {y_pred.shape}")

    # Loop through each city and hour for predictions
    for i in range(len(features)):
        city = features['city'][i]
        hour = str(features['Hour'][i])
        uvIndex = str(y_pred[i])[1:-2] # Remove brackets and comma
        forecast.append({'city': city, 'hour': hour, 'uvIndex': uvIndex})

    return forecast

if __name__ == '__main__':
    forecast_uv(debug=True)