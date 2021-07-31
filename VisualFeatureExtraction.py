# imports
import cv2
import colorsys
from sklearn.cluster import KMeans
import  utils
import numpy as np
from main import *


def create_cluster(filepath, cluster_centers):
    img = cv2.imread(filepath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1], 3))

    # cluster the pixels
    clt = KMeans(n_clusters=cluster_centers)
    clt.fit(img)

    return clt;


def create_hist(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    # return the histogram
    return hist


def read_and_convert_to_rgb(filepath):
    img = cv2.imread(filepath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img;


def reshape_imgdata(rgb_image):

    # reshape the image to become a list of pixels
    img = rgb_image.reshape((rgb_image.shape[0] * rgb_image.shape[1], 3))

    return img;


# Convert RGB into HSV


def convert_rgb_to_hsv(rgb_values):

    hsv_values = colorsys.rgb_to_hsv(rgb_values[0],rgb_values[1],rgb_values[2])

    return hsv_values;

# Convert RGB into HLS


def convert_rgb_to_hls(rgb_values):
    hsl_values = colorsys.rgb_to_hls(rgb_values[0],rgb_values[1],rgb_values[2]);

    return hsl_values;


# Grayscale image funktioniert!

def convert_rgb_to_grayscale(rgb_values):

    grayscale_img = cv2.cvtColor(rgb_values, cv2.COLOR_RGB2GRAY)

    return grayscale_img;


def get_brightness_value_of_rgb(filepath):

    img = cv2.imread(filepath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[0] * img.shape[1], 3))

    cols, rows = img.shape

    brightness = np.sum(img) / (255* cols * rows)

    return brightness;


def weighted_rgb_score(rgb_values, weights):

    red_value = rgb_values[0][0] * weights[0] + rgb_values[1][0] * weights[1] \
                + rgb_values[2][0] * weights[2] + rgb_values[3][0] * weights[3]

    green_value = rgb_values[0][1] * weights[0] + rgb_values[1][1] * weights[1] \
                + rgb_values[2][1] * weights[2] + rgb_values[3][1] * weights[3]

    blue_value = rgb_values[0][2] * weights[0] + rgb_values[1][2] * weights[1] \
                + rgb_values[2][2] * weights[2] + rgb_values[3][2] * weights[3]

    all_centers_rgb = [red_value, green_value, blue_value];

    # (r0 * w0) + (r1 * w1) + (r2 * w2) + (r3 * w3) = rweighted
    # (g0 * w0) + (g1 * w1) + (g2 * w2) + (g3 * w3) = gweighted
    # (b0 * w0) + (b1 * w1) + (b2 * w2) + (b3 * w3) = bweighted

    return all_centers_rgb;


# Get yellow value - intensity of yellow = rgb to cmyk and get brightness of only the y channel of the cmyk image

def get_yellow_value_of_rgb(filepath):

    img = plt.imread(filepath)

    bgr = img.astype(float) / 255.

    with np.errstate(invalid='ignore', divide='ignore'):
        K = 1 - np.max(bgr, axis=2)
        C = (1 - bgr[..., 2] - K) / (1 - K)
        M = (1 - bgr[..., 1] - K) / (1 - K)
        Y = (1 - bgr[..., 0] - K) / (1 - K)

    # Convert the input BGR image to CMYK colorspace
    CMYK = (np.dstack((C, M, Y, K)) * 255).astype(np.uint8)

    # Split CMYK channels
    Y, M, C, K = cv2.split(CMYK)

    np.isfinite(C).all()
    np.isfinite(M).all()
    np.isfinite(K).all()
    np.isfinite(Y).all()

    yellow = np.average(Y)

    return yellow;


def features_image (filepath, clt, hist):

    # rgb value

    rgb = weighted_rgb_score(clt, hist)

    rgb = utils.transfrom_255_to_1(rgb)

    # saturation

    saturation = convert_rgb_to_hsv(rgb)[1]

    # brightness

    brightness = get_brightness_value_of_rgb(filepath)

    # yellow

    yellow = get_yellow_value_of_rgb(filepath)

    yellow = utils.transform_yellow_255_to_1(yellow)

    image_vector = [rgb[0], rgb[1], rgb[2], saturation, brightness, yellow]

    return image_vector;
