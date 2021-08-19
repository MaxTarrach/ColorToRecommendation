import numpy
import math
from GetSpotify import *

from VisualFeatureExtraction import *


def normalize_songs(song_vectors):

    for i in range(len(song_vectors)):

        song_vectors[i, 1] = song_vectors[i, 1] / 11

        song_vectors[i, 2] = 1 - ((song_vectors[i, 2] * - 1) / 60)

        song_vectors[i, 5] = song_vectors[i, 5] / 160

    return song_vectors


def calculate_brightness_key(imageVector, songVectors, i):

    brightness = imageVector[4]
    key = songVectors[i, 1]

    brightness_key = (brightness - key)

    return brightness_key;


def calculate_brightness_tempo(imageVector, songVectors, i):

    brightness = imageVector[4]
    tempo = songVectors[i, 5]

    brightness_tempo = (brightness - tempo)

    return brightness_tempo


def calculate_brightness_loudness(imageVector, songVectors, i):

    brightness = imageVector[4]
    loudness = songVectors[i, 2]

    brightness_loudness = (brightness - loudness)

    return brightness_loudness


def calculate_saturation_tempo(imageVector, songVectors, i):

    saturation = imageVector[3]
    tempo = songVectors[i, 5]

    saturation_tempo = (saturation - tempo)

    return saturation_tempo;


def calculate_blue_key(imageVector, songVectors, i):

    blue = imageVector[2]
    key = songVectors[i, 1]

    blue_key = blue - (1 - key)

    return blue_key


def calculate_yellow_energy(imageVector, songVectors, i):

    yellow = imageVector[5]
    energy = songVectors[i, 0]

    yellow_energy = (yellow - energy)

    return yellow_energy


def calculate_color_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]
    blue = imageVector[2]
    yellow = imageVector[5]

    if mode == 0:
        color_mode = mode - (1 - yellow)

    else:
        color_mode = mode - blue

    return color_mode;


def calculate_saturation_mode(imageVector, songVectors, i):

    saturation = imageVector[3]
    mode = songVectors[i, 3]

    saturation_mode = mode - (1 - saturation)

    return saturation_mode;


def calculate_brightness_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]
    brightness = imageVector[4]

    brightness_mode = mode - (1 - brightness)

    return brightness_mode

def calculate_red_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]
    red = imageVector[0]

    red_mode = mode - (1 - red)

    return red_mode

def calculate_green_mode(imageVector, songVectors, i):

    mode = songVectors[i, 3]
    green = imageVector[1]

    green_mode = mode - green

    return green_mode

def calculate_blue_valence(imageVector, songVectors, i):

    valence = songVectors[i, 4]
    blue = imageVector[2]

    blue_valence = blue - (1 - valence )

    return blue_valence


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

        brightness_mode = abs(calculate_brightness_mode(imageVector, songVectors, i))

        red_mode = abs(calculate_red_mode(imageVector, songVectors, i))

        green_mode = abs(calculate_green_mode(imageVector, songVectors, i))

        blue_valence = abs(calculate_blue_valence(imageVector, songVectors, i))

        distance = math.sqrt(0.5 * brightness_key + 0.5 * brightness_tempo + 0.25 * brightness_loudness + saturation_tempo + 1 * blue_key + 1 * yellow_energy + 1 * color_mode + 0.25 * saturation_mode + 0.25 * brightness_mode + red_mode + green_mode + blue_valence)

        distance = 1 / (1 + distance)

        distance_measures.append(distance)

    return distance_measures;

# new distance measurements

def calculate_distances_slider(imageVector, songVectors, mood, intensity, tempo):

    distance_measures = []

    for i in range(len(songVectors)):
        # brightness_key = brightness key - (brightness_key * mood)
        brightness_key = abs(calculate_brightness_key(imageVector, songVectors, i))

        brightness_tempo = abs(calculate_brightness_tempo(imageVector, songVectors, i))

        #tempo

        brightness_tempo = brightness_tempo - (brightness_tempo * tempo)

        brightness_loudness = abs(calculate_brightness_loudness(imageVector, songVectors, i))

        saturation_tempo = abs(calculate_saturation_tempo(imageVector, songVectors, i))

        # tempo

        saturation_tempo = saturation_tempo - (saturation_tempo * tempo)

        blue_key = abs(calculate_blue_key(imageVector, songVectors, i))

        yellow_energy = abs(calculate_yellow_energy(imageVector, songVectors, i))

        #intensity

        yellow_energy = yellow_energy - (yellow_energy * intensity)

        color_mode = abs(calculate_color_mode(imageVector, songVectors, i))

        #mood
        color_mode = color_mode - (color_mode * mood)

        saturation_mode = abs(calculate_saturation_mode(imageVector, songVectors, i))

        # mood
        saturation_mode = saturation_mode - (saturation_mode * mood)

        brightness_mode = abs(calculate_brightness_mode(imageVector, songVectors, i))

        # mood
        brightness_mode = brightness_mode - (brightness_mode * mood)

        red_mode = abs(calculate_red_mode(imageVector, songVectors, i))

        green_mode = abs(calculate_green_mode(imageVector, songVectors, i))

        blue_valence = abs(calculate_blue_valence(imageVector, songVectors, i))

        distance = math.sqrt(0.5 * brightness_key + 0.5 * brightness_tempo + 0.25 * brightness_loudness + saturation_tempo + 1 * blue_key + 1 * yellow_energy + 1 * color_mode + 0.25 * saturation_mode + 0.25 * brightness_mode + red_mode + green_mode + blue_valence)

        distance = 1 / (1+ distance)

        distance_measures.append(distance)

    return distance_measures;




def sort_after_distances(songs, distances):
    a = numpy.array(distances)

    a_np = []

    for i in range(len(a)):
        a_np.append([a[i]])

    # add distances to arrays

    added = numpy.append(songs, a_np, 1)

    sorted_songs = added[(-added[:,8]).argsort()]

    #sorted_songs = added[added[:, 8].argsort()]

    return sorted_songs;


# Nicer to look at rating than just the pure distance
def calculate_rating(value):

    value = round(value * 100)

    value = str(value)

    value = value + '%'

    return value;


# Function to call from main that creates the sorted list we want to display
def getSortedList(image, clusterCenters, playlist):

    global visual_np

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


def getSliderList( playlist, mood, intensity, tempo):

    mood = mood / 100

    intensity = intensity / 100

    tempo = tempo / 100

    df_songs = get_song_features(playlist)

    songs_np = df_songs.to_numpy()

    distances = calculate_distances_slider(visual_np, normalize_songs(songs_np), mood, intensity, tempo)

    sortedlist = sort_after_distances(songs_np, distances)


    return sortedlist