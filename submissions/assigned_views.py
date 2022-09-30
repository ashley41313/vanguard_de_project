#assigned_views.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file contains the SQL queries to create the 
#3 views that were assigned: 
#Top (3) songs by artist in terms of duration_ms
#Top (10) artists in the database by # of followers
#Top (5) songs by artist in terms of tempo#
#it connects to the sqlite database 'spotify.db' and 
#stores the views there

import sqlite3

#connect to database 
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

#delete old views we might've created
c.execute("DROP VIEW IF EXISTS prompt1")
c.execute("DROP VIEW IF EXISTS prompt2")
c.execute("DROP VIEW IF EXISTS prompt3")

#Top (3) songs by artist in terms of duration_ms
c.execute("CREATE VIEW prompt1 AS \
SELECT * \
FROM ( \
    SELECT artist_id, \
        artist_name, \
        song_name, \
        track_id, \
        duration_ms, \
        DENSE_RANK() OVER (PARTITION BY artist_name ORDER BY duration_ms DESC) song_rank \
    FROM( \
        SELECT art.artist_name artist_name, \
                art.artist_id artist_id, \
                t.song_name song_name, \
                t.track_id track_id, \
                MAX(t.duration_ms) duration_ms \
        FROM artist art \
        JOIN album alb \
        ON art.artist_id = alb.artist_id \
        JOIN track t \
        ON alb.album_id = t.album_id \
        GROUP BY art.artist_name, t.song_name)t ) t1 \
WHERE song_rank IN (1,2,3)")

#Top (10) artists in the database by # of followers
c.execute("CREATE VIEW prompt2 AS \
SELECT artist_id, artist_name, external_url, followers \
FROM artist \
ORDER BY followers DESC \
LIMIT 10")

#Top (5) songs by artist in terms of tempo#
c.execute("CREATE VIEW prompt3 AS \
SELECT * \
FROM( \
    SELECT  artist_id, \
            artist_name, \
            song_name, \
            track_id, \
            DENSE_RANK() OVER (PARTITION BY artist_name ORDER BY tempo DESC) AS song_rank \
    FROM ( \
        SELECT  art.artist_id, \
                art.artist_name artist_name, \
                t.song_name song_name, \
                t.track_id track_id, \
                MAX(tf.tempo) tempo \
        FROM artist art \
        JOIN album alb \
        ON art.artist_id = alb.artist_id \
        JOIN track t \
        ON alb.album_id = t.album_id \
        JOIN track_feature tf \
        ON t.track_id = tf.track_id \
        GROUP BY art.artist_name, t.song_name)t \
)t1 \
WHERE song_rank IN (1,2,3,4,5)")

#close connection 
conn.commit()
c.close()