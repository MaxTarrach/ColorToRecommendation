import numpy
import math
from GetSpotify import *

from VisualFeatureExtraction import *


def normalize_songs(songVectors):

    for i in range(len(songVectors)):

        songVectors[i, 1] = songVectors[i, 1] / 11
        songVectors[i, 2] = songVectors[i, 2] / 60+1
        songVectors[i, 5] = songVectors[i, 5] / 200

    return songVectors


# calculate distance between visual features of image and every song #######VERSION 1##########
def calculate_distance(imageVector, songVectors):

    distance_measures = []

    for i in range(len(songVectors)):

        # brightness - key
        brightness_key = imageVector[4] - songVectors[i, 1]
        # brightness - tempo
        brightness_tempo = imageVector[4] - songVectors[i, 5]
        # brightnes - loudness
        brightness_loudness = imageVector[4] - songVectors[i, 2]
        # saturation - tempo
        saturation_tempo = imageVector[4] - songVectors[i, 5]
        # blue - mode (minor)
        blue_key = imageVector[2] - songVectors[i, 1]

        # primitive calculation
        distance = abs(brightness_key) + abs(brightness_tempo) + abs(brightness_loudness) + abs(saturation_tempo) + abs(blue_key)

        distance_measures.append(distance)

    return distance_measures;


# work on this - extend this version

def calculate_distances_2 (imageVector, songVectors):

    distance_measures = []

    for i in range(len(songVectors)):

        # euklidische Distanz für bild # jeden einzelnen song
        brightness_key = (imageVector[4] - songVectors[i, 1])**2

        brightness_tempo = (imageVector[4] - songVectors[i, 5])**2
        # brightnes - loudness
        brightness_loudness = (imageVector[4] - songVectors[i, 2])**2
        # saturation - tempo
        saturation_tempo = (imageVector[4] - songVectors[i, 5])**2
        # blue - mode (minor)
        blue_key = (imageVector[2] - songVectors[i, 1])**2

        distance = math.sqrt(brightness_key + brightness_tempo + brightness_loudness + saturation_tempo + blue_key)

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
def getSortedList(image,clusterCenters, playlist):

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


