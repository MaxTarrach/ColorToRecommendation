#imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as np


clientID = 'ccc96fcbf06745cd83257810bec7192d'
clientSecret = '18a8ee1b57b14c0cb1beceeeb82fd393'


username = '11134845287'


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret))


def get_playlist_id(playlist_string):

    start = playlist_string.find('https://open.spotify.com/playlist/') + len('https://open.spotify.com/playlist/')
    end = playlist_string.find('?')

    playlist_id = playlist_string[start:end]

    return playlist_id;


# get song ids from playlist
def extract_song_ids(playlist_string):

    playlist = get_playlist_id(playlist_string)

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
def get_song_features(playlist):

    playlist_id = get_playlist_id(playlist)

    array_of_ids = extract_song_ids(playlist)

    energy_array = [];
    key_array = [];
    loudness_array = [];
    mode_array = [];
    valence_array = [];
    tempo_array = [];
    key_full_number_array = [];
    id_array = [];

    af = sp.audio_features(array_of_ids)

    for i in range(len(array_of_ids)):

        energy_array.append(af[i].get('energy'))
        key_array.append(af[i].get('key'))
        loudness_array.append(af[i].get('loudness'))
        mode_array.append(af[i].get('mode'))
        valence_array.append(af[i].get('valence'))
        tempo_array.append(af[i].get('tempo'))
        key_full_number_array.append(af[i].get('key'))
        print(af[i].get('mode'))
        id_array.append(array_of_ids[i])

        d = {'energy': energy_array, 'key': key_array, 'loudness': loudness_array, 'mode': mode_array,
         'valence': valence_array, 'tempo': tempo_array,'key_full_number': key_full_number_array, 'id': id_array}

    df = np.DataFrame(data=d)
    return df


# Display Song name in table in GUI
def song_name_display(id):

    title = sp.track(id).get('name')

    return title;


# Display Artist name in table in GUI
def song_artist_display(id):

    name = sp.track(id).get('artist')

    return name;


# Display Song key beneath plot in GUI
def get_song_key(song_chroma_key):

    song_chroma_key = str(song_chroma_key)

    key_dictionary = {
        "0": "C",
        "1": "C#",
        "2": "D",
        "3": "D#",
        "4": "E",
        "5": "F",
        "6": "F#",
        "7": "G",
        "8": "G#",
        "9": "A",
        "10": "A#",
        "11": "B",
    }

    key = key_dictionary[song_chroma_key]

    key = str(key)

    return key;


# Display Song mode beneath plot in GUI
def get_song_mode(song_mode):

    song_mode = str(song_mode)

    mode_dictionary = {
        '0': 'Major',
        '1': 'Minor'
    }

    mode = mode_dictionary[song_mode]

    mode = str(mode)

    return mode



