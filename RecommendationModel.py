import numpy
from GetSpotify import *

# Euklidische Distanz zwishen Vektoren

# Standartisiert Vektoren

# imageArray = [red, blue, green, yellow, sättigung, brightness, lightness]


# Aufgabe = Erstes einfaches Model

# import image vector with all visual features needed

image = numpy.array((0.873, 0.44, 0.005, 0.4375, 0.99))





#import playlist dataframe with all audio features needed

df_songs = get_song_features(extract_song_ids(playlist))

songs_numpy = df_songs.to_numpy()

print(df_songs)

print(songs_numpy)

print(songs_numpy[1][1])



# calculate distance between visual features of image and every song

def calculate_distance(imageVector, songVectors):




    distance_measures = []

    return distance_measures;