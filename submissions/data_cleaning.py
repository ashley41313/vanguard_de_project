#data_cleaning.py
#author: Ashley Eckert ashley41313@hotmail.com
#This file contains the functions validate(date_text)
#and cleanAlbums(df). These functions are used to verify 
#dates are in the correct format and to remove different 
#versions of albums that would lead to many duplicate songs

import pandas as pd
import datetime

#input: date_text
#checks that a date is in 'YYYY-MM-DD format
#if not, and a year is given, appends 01-01 to the year
def validate(date_text):
    date = date_text
    try: 
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Album date format corrected...")
        
        if len(date_text) == 4:
            date = date_text+"-01-01"
        
    return date

#input: dataframe of album information
#This function removes duplicate albums from the dataframe 
#that have different names. Example: If there are two albums, 
#'Born To Die' and 'Born To Die- Special Edition', we only keep the 
#first one. This function checks to see if an album name is a substring 
#of another album, if it is and has a character that implies a 
#different version of the same album ('-', '(', '(Deluxe)') we delete 
#that album
def cleanAlbums(df):
    #tracks if reached end of dataframe
    finished = False

    #sort values by album name
    df = df.sort_values(by='album_name')
    df = df.reset_index(drop=True)

    #get the album in the next row over 
    df["next_album"] = df["album_name"].shift(-1)
    df["next_artist_id"] = df["artist_id"].shift(-1)

    for i in range(len(df)):
        #end of dataframe, exit function
        if df.iloc[[i]]['next_album'].isnull().values.any(): 
            break

        #compare album info with album below it 
        album_1 = df.iloc[[i]]['album_name'].item()
        album_2 = df.iloc[[i]]['next_album'].item()
        artist1_id = df.iloc[[i]]['artist_id'].item()
        artist2_id = df.iloc[[i]]['next_artist_id'].item()

        #check if the album in the row below includes the name of the album in this row
        #" (" or " -" or " D" or 
        while((album_1+" (") in album_2 or (album_1+" -") in album_2 or (album_1+" D") in album_2 \
            or (album_1+":") in album_2 or album_1+(" –") in album_2 and artist1_id == artist2_id):

            #update info before deleting row below
            df.at[i, "next_album"] = df.at[i+1, "next_album"]
            df.at[i, "next_artist_id"] = df.at[i+1, "next_artist_id"]

            #delete row below, and reset index 
            df = df.drop(i+1)
            df = df.reset_index(drop=True)

            #update variables            
            album_2 = df.iloc[[i]]['next_album'].item()
            artist2_id = df.iloc[[i]]['next_artist_id'].item()

            #if no next album, done traversing table 
            if df.iloc[[i]]['next_album'].isnull().values.any():
                finished = True
                break
   
        #done, exit
        if finished: 
            break

    #drop the rows we used to make edits
    df = df.drop(columns=['next_album', 'next_artist_id'])
    return df