#visualization1.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file plots a seaborn bar plot for the artists
#with the greatest average wait time between releases
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 


conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#get the top 5 artists with longest wait time between albums
df = pd.read_sql_query("""SELECT *
       FROM least_active_artists 
       ORDER BY avg_wait DESC 
       LIMIT 5""", conn)

#graph the least active artists with their average year gaps
sns.color_palette("flare", as_cmap=True)
gf = sns.barplot(df, x="artist_name", y="avg_wait", hue="popularity", dodge=False, palette="flare")
gf.set_title("Least Active Artists")
gf.set_ylabel("Years Between New Releases (Average)") 
gf.set_xlabel("Artist")

plt.show()