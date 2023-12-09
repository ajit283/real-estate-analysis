import pandas as pd
import folium
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import plotly.express as px
import os
from folium.plugins import HeatMap

# Load environment variables
load_dotenv()
# Database connection
db_uri = os.getenv("DATABASE_URL")  # Replace with your actual database URI
engine = create_engine(db_uri)

# SQL query to retrieve data
query = text(
    """SELECT "LATITUDE", "LONGITUDE", "PRICE", "LIVING_AREA" FROM data_geocoded"""
)  # Replace with your actual query

# Read data into a DataFrame
df = pd.read_sql_query(con=engine.connect(), sql=query)

# Ensure the data is in the correct format (float)
df["LATITUDE"] = df["LATITUDE"].astype(float)
df["LONGITUDE"] = df["LONGITUDE"].astype(float)

df["PRICEPERM2"] = df["PRICE"] / df["LIVING_AREA"]

agg_df = df.groupby(["LATITUDE", "LONGITUDE"]).agg({"PRICEPERM2": "mean"}).reset_index()

map_center = {
    "lat": df["LATITUDE"].mean(),  # You can also set a specific latitude
    "lon": df["LONGITUDE"].mean(),  # You can also set a specific longitude
}

# Create a map with a heatmap overlay
fig = px.scatter_mapbox(
    agg_df,
    lat="LATITUDE",
    lon="LONGITUDE",
    color="PRICEPERM2",
    color_continuous_scale=px.colors.sequential.Viridis,  # You can choose your own color scale
    size_max=40,
    size="PRICEPERM2",
    zoom=10,
    mapbox_style="carto-positron",
)


fig.show()
# # Create a map
# map_center = [df["LATITUDE"].mean(), df["LONGITUDE"].mean()]  # Center of the map
# map = folium.Map(location=map_center, zoom_start=12)

# heat_data = [[row["LATITUDE"], row["LONGITUDE"]] for index, row in df.iterrows()]
# HeatMap(heat_data, radius=10, blur=15, min_opacity=0.5).add_to(map)

# # Add markers
# for _, row in df.iterrows():
#     folium.Marker(location=[row["LATITUDE"], row["LONGITUDE"]]).add_to(map)

# # Display the map
# map.show_in_browser()
