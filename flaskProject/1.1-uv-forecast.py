import tensorflow as tf
import os
import datetime as dt
import pandas as pd
import numpy as np

def get_forecasted_uv():
    """
    Call parquet file to forecast hourly UV index for the current day
    :param: None
    :return: JSON file with forecasted UV index
    """
    pass

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

    # Create dataframe to store model features
    features = pd.DataFrame(columns=['city','hour','day','month','year'])