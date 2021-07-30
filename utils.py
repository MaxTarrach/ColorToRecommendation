# import the necessary packages
import numpy as np
import cv2


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def transfrom_255_to_1(value):

    r = value[0] / 255
    g = value[1] / 255
    b = value[2] / 255

    value_0_to_1= [r,g,b]

    return value_0_to_1

def transform_yellow_255_to_1(value):

    y = value / 255

    return y


def handle_spotify_link(link):
    link= ''

    return link