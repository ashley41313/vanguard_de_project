#visualization1.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file graphs the relationship between loudness and 
#energy for all songs. The darker the dot means the more 
#energy that songs has
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#plots the correlation between energy and loudness for songs 
df = pd.read_sql_query("""SELECT * FROM song_energy_rankings""", conn)
gf = sns.scatterplot(df, x="energy", y="loudness", hue="energy_ranking")
gf.set_title("Correlation Between Energy and Loudness In Songs")
plt.show()

