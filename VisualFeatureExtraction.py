# imports
import cv2
import colorsys


#Variablen

cluster_centers = 4;


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
    hsl_values = 1;

    return hsl_values;


#Grayscale image funktioniert!


def convert_rgb_to_grayscale(rgb_values):

    grayscale_img = cv2.cvtColor(rgb_values, cv2.COLOR_RGB2GRAY)

    return grayscale_img;


# Get yellow value - intensity of yellow = 1 - tristimulus value of blue

def get_yellow_value_of_rgb():

    yellow_value = 1;

    return yellow_value;


def weighted_rgb_score(rgb_values, weights):

    red_value = rgb_values[0][0] * weights[0] + rgb_values[1][0] * weights[1] \
                + rgb_values[2][0] * weights[2] + rgb_values[3][0] * weights[3]

    green_value = rgb_values[0][1] * weights[0] + rgb_values[1][1] * weights[1] \
                + rgb_values[2][1] * weights[2] + rgb_values[3][1] * weights[3]

    blue_value = rgb_values[0][2] * weights[0] + rgb_values[1][2] * weights[1] \
                + rgb_values[2][2] * weights[2] + rgb_values[3][2] * weights[3]

    all_centers_rgb = [red_value, green_value, blue_value];

    print('R :',  all_centers_rgb[0], 'G : ', all_centers_rgb[1], 'B : ', all_centers_rgb[2])

    # (r0 * w0) + (r1 * w1) + (r2 * w2) + (r3 * w3) = rweighted
    # (g0 * w0) + (g1 * w1) + (g2 * w2) + (g3 * w3) = gweighted
    # (b0 * w0) + (b1 * w1) + (b2 * w2) + (b3 * w3) = bweighted

    return all_centers_rgb;
