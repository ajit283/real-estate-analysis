import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

df = pd.read_csv('data/data_010423.csv')

df = df[df['COORD'].apply(lambda x: len(x) != 2)]


df['LAT'] = df['COORD'].apply(lambda x: ast.literal_eval(x)[0])
df['LONG'] = df['COORD'].apply(lambda x: ast.literal_eval(x)[1])

df['PRICE/LIVING_AREA'] = df['PRICE'] / df['LIVING_AREA']

print(df)

sns.scatterplot(x='LONG', y='LAT', hue='PRICE/LIVING_AREA', data=df)
# sns.regplot(x='LIVING_AREA', y='PRICE', data=df)

plt.show()
