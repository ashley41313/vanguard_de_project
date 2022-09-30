Author: Ashley Eckert
email: ashley41313@hotmail.com 
09-29-2022

OVERALL: 
This project pulls data from spotify for 20 artist.
For each artist, it pulls their album info,
for each album, it pulls track info and audio features. 
It processes the data pulled making sure it meets the standards
to be put into a local sqlite database. 
Then I created different views in the sqlite database to 
draw conclusions from the data collected. 

FILE INFO:
ingestion.py is the main file that pulls data from the spotify api, 
and creates data frames for each artist, album, track, and 
track_feature table. It includes helper functions getArtistInfo(artist), 
getArtistAlbums(artist_id, artist_uri), getTracks(album_id),
getTrackFeatures(track, name) which each stores information for an artist, 
album, track, track_feature into the appropriate table. 
The main() function makes the call to the helper functions and, after 
making all the calls, transforms the tables into dataframes 
which are then cleaned. main() returns these dataframes. 
After the main() function, I created the spotify.db file 
and turned the 4 dataframes(artist_df, album_df, track_df, track_feature df) 
into tables. 

data_cleaning.py is the file that contains 2 functions that clean and process 
data. It has a validate(date_text) function which checks every albums release_date
and makes sure it is in the YYYY-MM-MM format. It also has the cleanAlbums(df)
which processes all the albums in the albums_dataframe and removes duplicate 
albums that will cause redundancies and slow runtimes later on. 
It removes albums that habe a substring of another album by that same artist.
Example: If there are two albums 'Born To Die' and 'Born To Die: Deluxe' it 
removes the entry for 'Born To Die: Deluxe'. 

assigned_views.py is where I created the 3 sqlite views that were assigned and 
stored them into the database. 
VIEW prompt1: Top (3) songs by artist in terms of duration_ms
VIEW prompt2: Top (10) artists in the database by # of followers
VIEW prompt3: Top (5) songs by artist in terms of tempo#

customviews_1.py is where I create 3 different views. I store
them all in one file because each view builds on the last and they 
are related to each other. 
VIEW artist_songs_per_year: how many songs an artist released each 
                            year they were active
VIEW activity_gaps: For each year an artist was active (exclude their 
                    first year) calculate how long it has been since their 
                    last release artists that were only active 1 year are 
                    not included - because there is no time (year) gap 
VIEW least_active_artists:  artists with the longest average wait 
                            (in years) between music releases

customviews_2.py is where I create 3 different views. I store
them all in one file because each view builds on the last and they 
are related to each other. 
VIEW song_energy_rankings:  give an energy ranking for each song. 
                            basically strips energy value
VIEW artist_energy_totals:  the amount of songs an artist has in different 
                            energy rankings  
VIEW highest_energy_artists: Top (5) artists with the most energetic songs

visualization1.py: plots artists and the average wait times before they release
new music. 

visualization2.py: displays the top 5 artists with the longest wait time between
releases. 

visualization3.py: shows the correlation between a songs energy and loudness.

visualization4.py: For the 5 artists with the most energetic songs, it displays 
how many songs that arist has in each energy category. 

Comment: On the VIEWS I created, I kept the id correlated with the info I 
pulled (ex: if displaying top artists, i kept artist_id in the view) so 
that later on I could join my views with other tables using that id. 


The end :)