import numpy
from GetSpotify import *

from VisualFeatureExtraction import *

# Euklidische Distanz zwishen Vektoren

# Standartisiert Vektoren

# imageArray = [red, blue, green, yellow, sättigung, brightness, lightness]


# Aufgabe = Erstes einfaches Model

# import image vector with all visual features needed

image = numpy.array((0.873, 0.44, 0.005, 0.4375, 0.99))


#import playlist dataframe with all audio features needed

df_songs = get_song_features(extract_song_ids(playlist))

df_visual = features_image(image_file, create_cluster(image_file,cluster_centers).cluster_centers_,create_hist(create_cluster(image_file,cluster_centers)))


visual_np = numpy.array(df_visual)

print(visual_np)

songs_np = df_songs.to_numpy()

# Linear Mapping key ( x = key / 11)

songs_np[0, 1] = songs_np[0, 1] / 11

songs_np[1, 1] = songs_np[1, 1] / 11

songs_np[2, 1] = songs_np[2, 1] / 11


# Linear Mapping loudness

songs_np[0,2] = songs_np[0, 2] / 60 + 1

songs_np[1,2] = songs_np[1, 2] / 60 + 1

songs_np[2,2] = songs_np[2, 2] / 60 + 1

# Mapping tempo

songs_np[0, 5] = songs_np[0, 5] / 200

songs_np[1, 5] = songs_np[1, 5] / 200

songs_np[2, 5] = songs_np[2, 5] / 200

print(songs_np)

# calculate distance between visual features of image and every song

def calculate_distance(imageVector, songVectors):

    distance_measures = []

    for i in range(len(songVectors)):

        # brightness - key
        brightness_key = imageVector[4] - songVectors[i, 1]
        print('bk', brightness_key)
        # brightness - tempo
        brightness_tempo = imageVector[4] - songVectors[i, 5]
        print('bt', brightness_tempo)
        # brightnes - loudness
        brightness_loudness = imageVector[4] - songVectors[i, 2]
        print('bl', brightness_loudness)
        distance = abs(brightness_key) + abs(brightness_tempo) + abs(brightness_loudness)

        distance_measures.append(distance)

    return distance_measures;


distances = calculate_distance(visual_np, songs_np)

a = numpy.array(distances)

print(a)

print(a[1])

# add distances to arrays

added = numpy.append(songs_np, [[a[0]], [a[1]], [a[2]]], 1)

# sort array

sorted_songs = added[added[:, 7].argsort()]

print(sorted_songs)



