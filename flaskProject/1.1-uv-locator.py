import requests
import pandas as pd
import csv
import ast
import tensorflow as tf

## SOURCE:
## Melbourne data: https://data.gov.au/dataset/ds-dga-fb836013-f300-4f92-aa1e-fb5014aea40e/details?q=Ultraviolet%20Radiation%20Index
## Adelaide data: https://data.gov.au/dataset/ds-dga-026d4974-9efb-403d-9b39-27aee31a6439/details?q=Ultraviolet%20Radiation%20Index
## Perth data: https://data.gov.au/dataset/ds-dga-1b55352e-c0d8-48c8-9828-ef12885c9797/details?q=Ultraviolet%20Radiation%20Index
## Canberra data: https://data.gov.au/dataset/ds-dga-154d4d3b-2e8d-4dc2-b8ac-8f9805f99826/details?q=Ultraviolet%20Radiation%20Index
## Brisbane data: https://data.gov.au/dataset/ds-dga-2a1a2e49-de97-450e-9d0a-482adec68b22/details?q=Ultraviolet%20Radiation%20Index
## Sydney data: https://data.gov.au/dataset/ds-dga-c31a759c-a4d4-455f-87a7-98576be14f11/details?q=Ultraviolet%20Radiation%20Index
## OpenUV API: https://www.openuv.io/

def get_location(city_name):
    """
    Get the latitude and longitude for a given location
    :param name: Name of the location
    :return: Dictionary with 'lat' and 'lng' keys
    """
    # Open the CSV file
    with open("database/1.1/location.csv", "r") as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)

        # Initialize an empty dictionary to store data
        locations = {}

        # Loop through each row in the CSV file
        for row in reader:
            # Extract the city name as the key
            city = row["city"]

            # Convert the location string into a dictionary
            location_dict = ast.literal_eval(row["location"])

            # Add the city-location pair to the dictionary
            locations[city] = location_dict
    return locations[city_name]

def get_uv_index(city_name):
    """
    Get the UV index for a given location using the OpenUV API
    :param location: Dictionary with 'lat' and 'lng' keys
    :return: UV index as a float
    """
    # Get location lat and long data from the location.csv file
    location = get_location(city_name)

    # read OpenUV api from text file - DO NOT PUBLISH THE API KEY!
    # LIMIT OF 50 REQUESTS PER DAY!!
    with open('api/openuv-api.txt', 'r') as file:
        api_key = file.read()
    url = f"https://api.openuv.io/api/v1/uv?lat={location['lat']}&lng={location['lng']}"
    headers = {'x-access-token': api_key}
    response = requests.get(url, headers=headers)
    # If request succeeded, parse the JSON response
    if response.status_code == 200:
        uv_data = response.json()
        uv_index = uv_data['result']['uv']
        return uv_index
    else:
        print("Error fetching UV index:", response.status_code)
        return None
    
def get_forecasted_uv():
    """
    Call parquet file to forecast hourly UV index for the current day
    :param: None
    :return: JSON file with forecasted UV index
    """
    pass

# Example usage:
if __name__ == "__main__":
    print(get_uv_index('Melbourne'))