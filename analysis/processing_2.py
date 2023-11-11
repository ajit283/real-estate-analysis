import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import seaborn as sns
from datetime import datetime
import os



# formatted_date = datetime.now().strftime('%d%m%y')

# filename = "data_" + formatted_date + ".csv"

filename = "data_190823.csv"

df = pd.read_csv('../scraping/data/' + filename)

df = df[df['PRICE'] != 'auf Anfrage']

# print(df.head(5))


# Remove the € symbol and the dot from the price column
df['PRICE'] = df['PRICE'].str.replace(' €', '').str.replace('.', '').str.replace(',', '.').astype(float).round().astype(int)

# Remove the m² symbol from the size column
df['LIVING_AREA'] = df['LIVING_AREA'].str.replace(' m²', '').str.replace('.', '').str.replace(',', '.').astype(float)

print(df.head(5))


# Create the line plot
sns.lineplot(data=df, x='LIVING_AREA', y='PRICE')
sns.regplot(data=df, x='LIVING_AREA', y='PRICE', scatter=False, color='red')

# Display the plot
plt.show()