#visualization1.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file plots a seaborn barplot for the average time (years)
#an artist waits before releasing new music. 
#The artists are ordered from Top to Bottom, from Least Popular 
#to most Popular 
#The darker the bar is the more followers an artist has 
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

conn = sqlite3.connect('spotify.db')

#FIRST GRAPH
#get the least_active_artists table 
df = pd.read_sql_query("""SELECT *
        FROM least_active_artists 
        ORDER BY popularity DESC""", conn)

#graph the table to show all the artists average wait time between releases
sns.color_palette("flare", as_cmap=True)
gf = sns.barplot(df, x="avg_wait", y="artist_name", hue="followers", dodge=False, palette='flare')
gf.set_title("Average Wait For Artist To Release Music\nMost Popular Artist (T) - Least Popular Artist (B)")
gf.set_xlabel( "Years") 
gf.set_ylabel( "Artist")
plt.xticks(rotation=45)
plt.show()

