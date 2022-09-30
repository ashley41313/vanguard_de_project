#ingestion.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file, having a list of artists, generates tables 
#called rartist, album, track, and track_feature
#tables that store information for all artists 

#FUNCTIONS
#main() -> calls getArtistInfo(artist), getArtistAlbums(artist_id), getTracks(album_id)
#getArtistInfo(artist) -> adds a row to the ARTIST table for each artist 
#getArtistAlbums(artist_id) -> gets each album for that artist, adds a row 
#   for each album into the ALBUMS table 
#getTracks(album_id) -> gets all the tracks in an album, and add a row for each 
#   track into the TRACK table. 
#   calls getTrackFeature(track) on each track
#getTrackFeature(track) -> adds a row of the audio features for that track into the 
#   TRACK_FEATURE table

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import pandas as pd
import sqlite3
from data_cleaning import *

#connect to api 
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#GLOBAL VARIABLES
#holds the rows for artist/album/track/track_feature sqlite table
artists_table = [] 
albums_table = []
tracks_table = []
track_features_table = []
artists = ['Surf Curse', 'Mac Demarco', 'Vince Staples','FKA Twigs', 'Charli XCX', \
   'Lana Del Rey', 'Rihanna', 'Solange', 'The Marias', 'Frank Ocean', 'Yung Lean', \
       'Isaiah Rashad', 'Omar Apollo', 'Julia Jacklin', 'SZA', 'Khruangbin', 'Kid Cudi', \
           'Playboi Carti', 'Daniel Caesar', 'Lil Uzi Vert']


#input: artist returns: nothing
#gets artist info. creates a list with artist info for specific artist.
#that list is inserted as a row in the ARTIST table
def getArtistInfo(artist):
    artist_info = []
    artist_results = spotify.search(artist, type="artist", limit=1, market="US")

    #null check
    if artist_results is None:
        return 

    #grab the first artists values
    items = artist_results['artists']['items']
    artist = items[0]

    #add the info for this artist into a list 
    artist_info.append(artist['id'])
    artist_info.append(artist['name'])
    artist_info.append(artist['external_urls']['spotify'])
    artist_info.append(artist['genres'][0])
    artist_info.append(artist['images'][0]['url'])
    artist_info.append(artist['followers']['total'])
    artist_info.append(artist['popularity'])
    artist_info.append(artist['type'])
    artist_info.append(artist['uri'])

    #adds the list as a row into the ARTIST table 
    artists_table.append(artist_info)

#input: artist_id, artist_uri 
#given an artist_id, this function finds all albums by this artist. 
#for each album, it stores that albums info into a list and stores 
#that list as a row in the ALBUM table
def getArtistAlbums(artist_id, artist_uri): 
    albums = spotify.artist_albums(artist_id, album_type='album', limit=50, country='US')

    #null check
    if albums is None: 
        return 
    
    albums = albums['items']

    #for each album, append album info as a row in ALBUMS table
    for i in range(len(albums)):
        album = albums[i] #next album

        #create list for album info 
        album_info = []
        album_info.append(album['id'])
        album_info.append(album['name'])
        album_info.append(album['external_urls']['spotify'])
        album_info.append(album['images'][0]['url'])
        album_info.append(validate(album['release_date']))
        album_info.append(album['total_tracks'])
        album_info.append(album['type'])
        album_info.append(album['uri'])
        album_info.append(artist_id)

        #append list of album info into a list of this artists albums
        albums_table.append(album_info)
    

#input: album_id 
#given an album_id, get track info for each track 
#for each track in that album, create a list of track info
#and append it as a row in the TRACKS table.
#calls the getTrackFeatures() function on each track
def getTracks(album_id):
    #get tracks info for that album 
    tracks = spotify.album_tracks(album_id)

    #null check
    if tracks is None:
        return 

    tracks = tracks['items']

    #iterate through each track 
    for i in range(len(tracks)): 
        curr_track = tracks[i]

        #store track info into a list 
        track_info = []
        track_info.append(curr_track['id'])
        track_info.append(curr_track['name'])
        track_info.append(curr_track['external_urls']['spotify'])
        track_info.append(curr_track['duration_ms'])
        track_info.append(curr_track['explicit'])
        track_info.append(curr_track['disc_number'])
        track_info.append(curr_track['type'])
        track_info.append(curr_track['uri'])
        track_info.append(album_id)

        #add this track into the TRACKS table
        tracks_table.append(track_info)

        #get track features for this track 
        getTrackFeatures(curr_track['id'], curr_track['name'])


#gets called inside the getTracks function. 
#input: track
#given a track, grabs that tracks features into a list 
#and appends that list as a row in the TRACK_FEATURES table
def getTrackFeatures(track, name):
    #get the track features JSON object 
    track_features = spotify.audio_features(track)
    track = track_features[0]

    #if no audio features, skip this song 
    if track is None:
        return 
    
    #create list filled with this tracks features 
    curr_track_features = []
    curr_track_features.append(track['id'])
    curr_track_features.append(track['danceability'])
    curr_track_features.append(track['energy'])
    curr_track_features.append(track['instrumentalness'])
    curr_track_features.append(track['liveness'])
    curr_track_features.append(track['loudness'])
    curr_track_features.append(track['speechiness'])
    curr_track_features.append(track['tempo'])
    curr_track_features.append(track['type'])
    curr_track_features.append(track['valence'])
    curr_track_features.append(track['uri'])

    #append track features as a row in TRACK_FEATURES table 
    track_features_table.append(curr_track_features)

def main():
    #PART 1: for each artist, call getArtistInfo()
    for artist in artists: 
        getArtistInfo(artist)

    #turn ARTIST table into a dataframe.
    artist_df = pd.DataFrame(artists_table, columns =['artist_id', 'artist_name', 
        'external_url', 'genre', 'image_url', 
        'followers', 'popularity', 'type', 'artist_uri'])
    print("Artist dataframe complete.")

    #PART 2: populate ALBUMS table 
    #grab all the artists who's albums we want
    artist_ids = list(artist_df['artist_id'])
    artist_uris = list(artist_df['artist_uri'])

    #for each artist call getArtistAlbums() function.
    for i in range(len(artist_ids)):
        getArtistAlbums(artist_ids[i], artist_uris[i])

    #ALBUMS table is finished, can convert to a dataframe 
    albums_df = pd.DataFrame(albums_table, columns =['album_id', 'album_name', 
        'external_url', 'image_url', 'release_date', 'total_tracks',
        'type', 'album_uri', 'artist_id'])
    print("Album dataframe complete.")

    #clean and remove duplicates from the dataframe 
    albums_df = albums_df.drop_duplicates(subset=['album_name'])
    albums_df = cleanAlbums(albums_df)

    #PART 3 and 4, populate the TRACKS and TRACK_FEATURES table 
    #grab all the albums for which we will find their tracks 
    album_ids = list(albums_df['album_id'])

    #for each album call getTracks()
    for i in range(len(album_ids)):
        getTracks(album_ids[i])

    #TRACKS and TRACK_FEATURES table are filled, so create dataframes for them 
    tracks_df = pd.DataFrame(tracks_table, columns =['track_id', 'song_name', 
        'external_url', 'duration_ms', 'explicit', 'disc_number',
        'type', 'song_uri', 'album_id'])

    track_features_df = pd.DataFrame(track_features_table, columns =['track_id', 'danceability', 
        'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
        'type', 'valence', 'song_uri'])
    print("Track and Track_feature dataframe complete.")

    return artist_df, albums_df, tracks_df, track_features_df

#main function call
artist_df, albums_df, tracks_df, track_features_df = main()

#create and save tables into sqlite database 
conn = sqlite3.connect('spotify.db')
c = conn.cursor()
print("spotify.db created")

c.execute('CREATE TABLE IF NOT EXISTS artist (artist_id varchar, artist_name varchar, \
        external_url varchar, genre varchar, image_url varchar, followers int, \
        popularity int, type varchar, artist_uri varchar)')

c.execute('CREATE TABLE IF NOT EXISTS album (album_id varchar, album_name varchar, \
        external_url varchar, image_url varchar, release_date date, \
        total_tracks int, type varchar, album_uri varchar, artist_id varchar)')

c.execute('CREATE TABLE IF NOT EXISTS track (track_id varchar, song_name varchar, \
        external_url varchar, duration_ms int, explicit boolean, disc_number int, \
        type varchar, song_uri varchar, album_id varchar)')

c.execute('CREATE TABLE IF NOT EXISTS track_feature (track_id varchar, danceability double, \
        energy double, instrumentalness double, liveness double, loudness double, \
        speechiness double, tempo double, type varchar, valence double, song_uri varchar)')

#convert the dataframes into sqlite tables
artist_df.to_sql('artist', conn, if_exists='replace', index = False)
albums_df.to_sql('album', conn, if_exists='replace', index = False)
tracks_df.to_sql('track', conn, if_exists='replace', index = False)
track_features_df.to_sql('track_feature', conn, if_exists='replace', index = False)
print("artist, album, track, and track_feature sqlite table created")

conn.commit()
conn.close()
