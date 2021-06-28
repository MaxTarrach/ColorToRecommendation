# Spotify test

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as np

# get a playlist and get features needed for analysis

clientID = 'ccc96fcbf06745cd83257810bec7192d'
clientSecret = '18a8ee1b57b14c0cb1beceeeb82fd393'

playlistLink = '0cubuWEaRYj2CUCOSkfrIq'



sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret))

song_features1 = sp.audio_features('0nqL2NizWKtQDpmr4A89eL')

song_features2 = sp.audio_features('5FXhWNvWuYk9cuEnS6K9PV')

song_features3 = sp.audio_features('1vjmuZ6Avr9H4tNoD74FXL')


#Dataframe aus Song/Playlist erstellen

def get_dataframe_for_playlist(test):

    d = {'energy': [0.154, 0.28, 0.117], 'key': [4, 2, 2], 'loudness': [-16.712, -18.539, -17.217], 'mode': [0, 1, 1],
         'valence': [0.0573, 0.569, 0.15], 'tempo': [72.691, 119.176, 134.839]}

    df = np.DataFrame(data=d)

    print(test)
    return df


def add_function(x):
    return 5 * x


print(get_dataframe_for_playlist(0))


# id of every song from playlist

def get_ids_from_playlist(playlistID):

    array_of_ids = [];


    return array_of_ids;
