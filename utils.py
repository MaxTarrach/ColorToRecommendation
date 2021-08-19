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