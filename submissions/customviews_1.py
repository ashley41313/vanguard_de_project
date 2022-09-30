#customviews1.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file contains the SQL queries to create three 
#different views. They're all in this one file because 
#each view builds on the last. 
#'artist_songs_per_year' shows how many songs an artist 
#released each year they were active 
#'activity_gaps' shows for each year an artist was active,
#how many years ago was their last release 
#'least_active_artists' shows artists with the longest average 
# wait (in years) between music releases, ordered from longest
# wait descending. 
 
import sqlite3

#connect to database 
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#drop views if we made it previously
c.execute("DROP VIEW IF EXISTS artist_songs_per_year")
c.execute("DROP VIEW IF EXISTS activity_gaps")
c.execute("DROP VIEW IF EXISTS least_active_artists")

#artist_songs_per_year
#displays how many songs an artist released each year they were active
# ...
#This table is used as a subquery in the next created table - album_gaps
c.execute("CREATE VIEW artist_songs_per_year AS \
SELECT  artist_id, \
        artist_name, \
        genre, \
        popularity, \
        followers, \
        year, \
        COUNT(DISTINCT song_name) songs_dropped \
FROM (  SELECT art.artist_id, \
                art.artist_name, \
                art.genre, \
                alb.album_name, \
                strftime('%Y', alb.release_date) year, \
                t.song_name, \
                art.popularity, \
                art.followers \
        FROM artist art \
        JOIN album alb \
        ON art.artist_id = alb.artist_id \
        JOIN track t \
        ON t.album_id = alb.album_id)t \
GROUP BY artist_name, year")

# For each year an artist was active (exclude their first year) 
# calculate how long it has been since their last release
# artists that were only active 1 year are not included - 
# because there is no time (year) gap 
c.execute("CREATE VIEW activity_gaps AS \
SELECT * \
FROM (  SELECT *, \
                year - (LAG(year, 1, 0) OVER (PARTITION BY artist_name ORDER BY year)) yrs_since_last_album \
        FROM artist_songs_per_year \
        ORDER BY popularity DESC, artist_name, year)t \
WHERE year - yrs_since_last_album != 0")


#Artists with the longest average wait (in years) between music releases
c.execute("CREATE VIEW least_active_artists AS \
SELECT artist_id, artist_name, genre, popularity, followers, AVG(yrs_since_last_album) avg_wait \
FROM activity_gaps \
GROUP BY 1 \
ORDER BY avg_wait DESC")

#close connection
conn.commit()
c.close()