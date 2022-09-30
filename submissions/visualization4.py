#visualization1.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file graphs a seaborn barplot 
#it picks the top 5 artists with the most energy 
#and shows how many songs each artist has in each
#energy level 
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#For the top 5 artists with the most energetic songs, 
#show how many songs they have in each energy level
df = pd.read_sql_query("""SELECT *
        FROM artist_energy_totals
        WHERE artist_name IN (SELECT artist_name FROM highest_energy_artists)""", conn)
gf = sns.barplot(df, x="energy_ranking", y="total_songs", hue="artist_name")
gf.set_title("Different Energy Rankings for Top Energetic Artists")
gf.set_xlabel( "Energy Level") 
gf.set_ylabel( "Song Count")
plt.show()

c.close()