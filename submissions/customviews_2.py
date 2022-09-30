#customviews2.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file contains the SQL queries to create three 
#different views. They're all in this one file because 
#each view builds on the last. 
#'song_energy_rankings' gives an energy ranking for each song 
# from 0-9
#'artist_energy_totals' shows how many songs in each level an
# artist has
#'highest_energy_artists' - the Top (5) artists with the most 
# songs with an energy ranking of 9 (highest)

import sqlite3

#connect to database
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#delete previously created views
c.execute("DROP VIEW IF EXISTS song_energy_rankings")
c.execute("DROP VIEW IF EXISTS artist_energy_totals")
c.execute("DROP VIEW IF EXISTS highest_energy_artists")

#give an energy ranking for each song. 
#basically strips energy value
c.execute("CREATE VIEW song_energy_rankings AS \
SELECT  art.artist_id,\
        art.artist_name, \
        t.song_name, \
        tf.energy, \
        CASE    WHEN tf.energy < .1 THEN 0 \
                WHEN tf.energy < .2 AND tf.energy > .1 THEN 1 \
                WHEN tf.energy < .3 AND tf.energy > .2 THEN 2 \
                WHEN tf.energy < .4 AND tf.energy > .3 THEN 3 \
                WHEN tf.energy < .5 AND tf.energy > .4 THEN 4 \
                WHEN tf.energy < .6 AND tf.energy > .5 THEN 5 \
                WHEN tf.energy < .7 AND tf.energy > .6 THEN 6 \
                WHEN tf.energy < .8 AND tf.energy > .7 THEN 7 \
                WHEN tf.energy < .9 AND tf.energy > .8 THEN 8 \
                WHEN tf.energy < 1 AND tf.energy > .9 THEN 9 \
                ELSE 0 END AS energy_ranking, \
        art.popularity, \
        tf.loudness, \
        tf.tempo \
FROM artist art \
JOIN album alb \
ON art.artist_id = alb.artist_id \
JOIN track t \
ON alb.album_id = t.album_id \
JOIN track_feature tf \
ON tf.track_id = t.track_id")

#the amount of songs an artist has in different energy rankings  
c.execute("CREATE VIEW artist_energy_totals AS \
SELECT artist_id, \
    artist_name, \
    energy_ranking, \
    COUNT(*) total_songs, \
    popularity \
FROM song_energy_rankings \
GROUP BY 1, 3 \
ORDER BY 3 DESC, 4 DESC")

#Top (5) artists with the most energetic songs
c.execute("CREATE VIEW highest_energy_artists AS \
SELECT artist_id, \
        artist_name, \
        energy_ranking, \
        total_songs \
FROM artist_energy_totals \
WHERE energy_ranking = 9 \
ORDER BY total_songs DESC \
LIMIT 5")

conn.commit()
c.close()