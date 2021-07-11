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

songs_np = df_songs.to_numpy()

# Linear Mapping key ( x = key / 11)

songs_np[0, 1] = songs_np[0, 1] / 11
print(songs_np[0, 1])
songs_np[1, 1] = songs_np[1, 1] / 11
print(songs_np[1, 1])
songs_np[2, 1] = songs_np[2, 1] / 11
print(songs_np[2, 1])


# calculate distance between visual features of image and every song

def calculate_distance(imageVector, songVectors):

    distance_measures = []

    for i in range(len(songVectors)):

        # image vector - song vectors
        distance = imageVector[4] - songVectors[i, 1]

        distance_measures.append(distance)

    return distance_measures;


distances = calculate_distance(visual_np, songs_np)

print(distances)
