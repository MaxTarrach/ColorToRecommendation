# Spotify test

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as np
import re
from pprint import pprint
import json

# get a playlist and get features needed for analysis

clientID = 'ccc96fcbf06745cd83257810bec7192d'
clientSecret = '18a8ee1b57b14c0cb1beceeeb82fd393'


username = '11134845287'
playlist = '0cubuWEaRYj2CUCOSkfrIq'


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret))


# get song ids from playlist

def extract_song_ids(playlist):

    sp_playlist = sp.playlist_items(playlist_id=playlist, fields='items.track.id', limit=100, offset=0, market=None,
                                    additional_types=['track'])
    tracks = sp_playlist['items']

    array_of_ids = [];

    for i in tracks:
        j = i.get('track')
        iden = j.get('id')

        array_of_ids.append(iden)

    return array_of_ids;

# Create a DataFrame with audio features from an array of song ids

def get_song_features(array_of_ids):

    energy_array = [];
    key_array = [];
    loudness_array = [];
    mode_array = [];
    valence_array = [];
    tempo_array = [];
    id_array = [];

    af = sp.audio_features(extract_song_ids(playlist))

    for i in range(len(array_of_ids)):

        energy_array.append(af[i].get('energy'))
        key_array.append(af[i].get('key'))
        loudness_array.append(af[i].get('loudness'))
        mode_array.append(af[i].get('mode'))
        valence_array.append(af[i].get('valence'))
        tempo_array.append(af[i].get('tempo'))
        id_array.append(array_of_ids[i])

        d = {'energy': energy_array, 'key': key_array, 'loudness': loudness_array, 'mode': mode_array,
         'valence': valence_array, 'tempo': tempo_array, 'id': id_array}

    df = np.DataFrame(data=d)
    return df


#print(type(song_features1))

#print(song_features1[0])

#print(song_features1)

#print(extract_song_ids(playlist))