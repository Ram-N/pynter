# utility functions
import math
import random
import sys
import time
import pyautogui as pg


WAIT_SECONDS = 5
VERBOSE = False

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


BRUSH_STYLES = {
    "brush": (1, 1),
    "callig brush1": (1, 2),
    "callig brush2": (1, 3),
    #    "Airbrush": (1, 4),
    #    "oil": (2, 1),
    "crayon": (2, 2),
    "marker": (2, 3),
    "pencil": (2, 4),
    "watercolor": (3, 1),
}

BRUSH_SIZES = {"8px": 0, "16px": 1, "30px": 2, "40px": 3}


def wait_loop(wait_time):
    print("Press Enter to start countdown")
    input()
    count = wait_time
    while count > 0:
        print(str(count) + "...", end=" ", flush=True)
        time.sleep(1)
        count -= 1
    print()


def capture_coords(btn, pretext="", posttext=""):
    """ Generic function to return location of a single item in MSP """
    print(pretext)
    wait_loop(WAIT_SECONDS)
    print(posttext)
    return pg.position()


def get_4_points(wait_time=5):

    for _ in range(4):
        wait_loop(wait_time)
        print(pg.position())


def get_coords(repeat):
    for _ in range(repeat):
        print(pg.position())
        time.sleep(1)


def is_invalid(art_direction, cv):
    """CHeck if the art directions are implementable."""
    llen = art_direction["LINE_LENGTH"]["line_length"]
    if llen[0].isnumeric():
        if int(llen[0]) > cv.width:
            print("Very high LINE LENGTH")
            return True
    return False


def get_active_brushes(art_direction):

    active_brushes = {}
    for v in art_direction["BRUSHES"].values():
        active_brushes[v[0]] = BRUSH_STYLES[v[0]]
    return active_brushes


def get_color_index_dict(color_list):
    """ Returns a dictionary of Colors and btn_indices, based on the color_list provided"""
    print(color_list)
    print([(k in ALL_COLORS) for k in color_list])
    return dict((k, ALL_COLORS[k]) for k in color_list if k in ALL_COLORS)


def is_pt_outside_canvas(cv, x, y):
    """ Returns 0 if pt is inside the canvas boundaries else returns 1 """

    if x >= cv.origin[0] and (x <= cv.endpoint[0]):
        if y >= cv.origin[1] and (y <= cv.endpoint[1]):
            return 0  # everything is okay
    return 1


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
