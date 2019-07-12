import pandas as pd
import matplotlib.pyplot as plot
df=pd.read_csv('dominant_topics.csv')


print(df.head())
print(df['Dominant_Topic'])