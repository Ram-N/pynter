# utility functions
import math
import random


ALL_COLORS = {
    "black": (1, 1),
    "gray50": (2, 1),
    "darkred": (3, 1),
    "red": (4, 1),
    "orange": (5, 1),
    "yellow": (6, 1),
    "green": (7, 1),
    "turquoise": (8, 1),
    "blue": (9, 1),
    "purple": (10, 1),
    "white": (1, 2),
    "gray25": (2, 2),
    "brown": (3, 2),
    "rose": (4, 2),
    "gold": (5, 2),
    "light-yellow": (6, 2),
    "lime": (7, 2),
    "light turquoise": (8, 2),
    "blue-gray": (9, 2),
    "lavender": (10, 2),
}


def get_palette(color_list):
    """ Returns a dictionary of Colors and btn_indices, based on the color_list provided"""
    return dict((k, ALL_COLORS[k]) for k in color_list if k in ALL_COLORS)


def get_start_pt(cv, art_direction, specific=""):
    """Return X Y coords per art_direction directives specified"""
    if specific == "random":
        startX = random.randint(cv.origin[0], cv.endpoint[0])
        startY = random.randint(cv.origin[1], cv.endpoint[1])
        return startX, startY


def get_stroke_endpoint(cv, art_direction, startX, startY, specific=""):
    """ Returns endX and endY points per directives

        if StartX and startY are specified, they will be used
        Length plays an important role. It should be specified inside art_direction
        Length can be completely 'random' or,
        Length can be {'Long', 'Med|ium' or 'short} or an exact number of pixels or,
        Length can be an exact number of pixels or,
        Length can be a range (between (min, max)).
        Angle & length if specified will be used
    """
    safety = 0
    found = 0

    llen = art_direction["LINE_LENGTH"]["line_length"]
    while not found:
        safety += 1
        if safety > 100:
            found = 1
            print("unable to find endx, endy")
            break

        if "random" in llen:
            stroke_len_x = random.randint(0, cv.width)
            stroke_len_y = random.randint(0, cv.height)
            end_x = random.choice([startX - stroke_len_x, startX + stroke_len_x])
            end_y = random.choice([startY - stroke_len_y, startY + stroke_len_y])

        if llen[0].isnumeric():
            stroke_len = int(llen[0])
            theta = math.radians(
                random.randint(-180, 180)
            )  # in radians, converted from degrees
            end_x = startX + int(stroke_len * math.cos(theta))
            end_y = startY + int(stroke_len * math.sin(theta))
        if end_x > cv.endpoint[0]:
            continue
        elif end_x < cv.origin[0]:
            continue
        elif end_y > cv.endpoint[1]:
            continue
        elif end_y < cv.origin[1]:
            continue
        else:
            found = 1

    return (end_x, end_y)


def as_dict(config):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict
