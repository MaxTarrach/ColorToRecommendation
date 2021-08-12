import numpy
import math
from GetSpotify import *

from VisualFeatureExtraction import *


def normalize_songs(song_vectors):

    for i in range(len(song_vectors)):

        song_vectors[i, 1] = song_vectors[i, 1] / 11
        song_vectors[i, 2] = song_vectors[i, 2] / 60
        song_vectors[i, 5] = song_vectors[i, 5] / 200

    return song_vectors


def calculate_brightness_key(imageVector, songVectors, i):

    brightness_key = (imageVector[4] - songVectors[i, 1])**2

    return brightness_key;


def calculate_brightness_tempo(imageVector, songVectors, i):

    brightness_tempo = (imageVector[4] - songVectors[i, 5]) ** 2

    return brightness_tempo


def calculate_brightness_loudness(imageVector, songVectors, i):

    brightness_loudness = (imageVector[4] - songVectors[i, 2]) ** 2

    return brightness_loudness


def calculate_saturation_tempo(imageVector, songVectors, i):

    saturation_tempo = (imageVector[3] - songVectors[i, 5]) ** 2

    return saturation_tempo;


def calculate_blue_key(imageVector, songVectors, i):

    blue_key = (imageVector[2] - songVectors[i, 1]) ** 2

    return blue_key


def calculate_yellow_energy(imageVector, songVectors, i):

    yellow_energy = (imageVector[5] - songVectors[i, 0]) ** 2

    return yellow_energy


def calculate_color_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]

    if mode == 0:
        color_mode = mode - imageVector[2]

    else:
        color_mode = mode - imageVector[5]

    return color_mode;


def calculate_saturation_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]

    saturation_mode = mode - imageVector[3]

    return saturation_mode;


def calculate_distances_2 (imageVector, songVectors):

    distance_measures = []

    for i in range(len(songVectors)):

        brightness_key = abs(calculate_brightness_key(imageVector, songVectors, i))

        brightness_tempo = abs(calculate_brightness_tempo(imageVector, songVectors, i))

        brightness_loudness = abs(calculate_brightness_loudness(imageVector, songVectors, i))

        saturation_tempo = abs(calculate_saturation_tempo(imageVector, songVectors, i))

        blue_key = abs(calculate_blue_key(imageVector, songVectors, i))

        yellow_energy = abs(calculate_yellow_energy(imageVector, songVectors, i))

        color_mode = abs(calculate_color_mode(imageVector, songVectors, i))

        saturation_mode = abs(calculate_saturation_mode(imageVector, songVectors, i))

        distance = math.sqrt(brightness_key + brightness_tempo + brightness_loudness + saturation_tempo + blue_key + yellow_energy + color_mode + saturation_mode)

        distance = 1 / (1 + distance)

        distance_measures.append(distance)

    return distance_measures;


def sort_after_distances(songs, distances):
    a = numpy.array(distances)

    a_np = []

    for i in range(len(a)):
        a_np.append([a[i]])

    # add distances to arrays

    added = numpy.append(normalize_songs(songs), a_np, 1)

    # sort array

    sorted_songs = added[added[:, 7].argsort()]

    return sorted_songs;


# Nicer to look at rating than just the pure distance
def calculate_rating(sortedList):
    ratings = []

    return ratings;


# Function to call from main that creates the sorted list we want to display
def getSortedList(image, clusterCenters, playlist):

    # audio_df = GetSpotify.playlist(playlist)
    df_songs = get_song_features(playlist)
    # visual_df = VisualFeatureExtraction(image)
    df_visual = features_image(image, create_cluster(image, clusterCenters).cluster_centers_,
                               create_hist(create_cluster(image, clusterCenters)))

    visual_np = numpy.array(df_visual)

    songs_np = df_songs.to_numpy()

    distances = calculate_distances_2(visual_np, normalize_songs(songs_np))

    sortedlist = sort_after_distances(songs_np, distances)

    return sortedlist;


