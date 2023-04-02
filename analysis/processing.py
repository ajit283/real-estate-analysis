import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def geocoding(address):
	api_key = os.getenv('GMAPS_API_KEY') 
    	# Set the API endpoint and parameters
	url = 'https://maps.googleapis.com/maps/api/geocode/json'
	params = {'address': address, 'key': api_key}

	# Make a GET request to the API endpoint
	response = requests.get(url, params=params)

	# Parse the JSON response
	data = response.json()

	# Extract the latitude and longitude coordinates
	lat = data['results'][0]['geometry']['location']['lat']
	lng = data['results'][0]['geometry']['location']['lng']

	return (lat,lng)

filename = "data_010423.csv"

df = pd.read_csv('../scraping/data/' + filename)

df = df[df['PRICE'] != 'auf Anfrage']

print(df.head(5))


# Remove the € symbol and the dot from the price column
df['PRICE'] = df['PRICE'].str.replace(' €', '').str.replace('.', '').astype(int)

# Remove the m² symbol from the size column
df['LIVING_AREA'] = df['LIVING_AREA'].str.replace(' m²', '').str.replace(',', '.').astype(float)

print(df.head(5))

# Create a new column for the latitude and longitude coordinates
df['COORD'] = df['LOCATION'].apply(geocoding)

# Save the dataframe to a CSV file
df.to_csv('./data/' + filename, index=False)

print(df)