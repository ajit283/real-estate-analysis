import pandas as pd
import requests
import os
from datetime import datetime
from sqlalchemy import create_engine

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Database connection
db_uri = os.getenv(
    "DATABASE_URL"
)  # Example: 'postgresql://username:password@localhost:5432/mydatabase'
engine = create_engine(db_uri)


def geocoding(address):
    api_key = os.getenv("GMAPS_API_KEY")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    lat = data["results"][0]["geometry"]["location"]["lat"]
    lng = data["results"][0]["geometry"]["location"]["lng"]
    return (lat, lng)


filenames = ["data_281023.csv"]
for filename in filenames:
    # Load and preprocess the dataframe
    formatted_date = datetime.now().strftime("%d%m%y")
    filename = "data_281023.csv"
    df = pd.read_csv("../scraping/data/" + filename)
    df = df[df["PRICE"] != "auf Anfrage"]

    df["PRICE"] = (
        df["PRICE"]
        .str.replace(" €", "")
        .str.split(",")
        .str[0]
        .str.replace(".", "")
        .astype(int)
    )
    df["LIVING_AREA"] = (
        df["LIVING_AREA"]
        .str.replace(" m²", "")
        .str.replace(".", "")
        .str.replace(",", ".")
        .astype(float)
    )

    df = df.head(100)

    df[["LATITUDE", "LONGITUDE"]] = df["LOCATION"].apply(geocoding).apply(pd.Series)

    # Append to PostgreSQL table
    df["date"] = datetime.strptime(
        filename.split("_")[1].split(".")[0], "%d%m%y"
    ).date()
    df.to_sql("data_geocoded", engine, if_exists="append", index=False)
