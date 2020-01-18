# utility functions
import math
import random
import sys
import time

import pyautogui as pg

WAIT_SECONDS = 5



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


def get_color_index_dict(color_list):
    """ Returns a dictionary of Colors and btn_indices, based on the color_list provided"""
    print(color_list)
    print([(k in ALL_COLORS) for k in color_list])
    return dict((k, ALL_COLORS[k]) for k in color_list if k in ALL_COLORS)


def get_start_pt(cv, art_direction, specific=""):
    """Return X Y coords per art_direction directives specified"""
    if specific == "random":
        startX = random.randint(cv.origin[0], cv.endpoint[0])
        startY = random.randint(cv.origin[1], cv.endpoint[1])
        print(f'starting at {startX} {startY}')
        return startX, startY


def is_pt_outside_canvas(cv, x, y):
    """ Returns 0 if pt is inside the canvas boundaries else returns 1 """

    if x > cv.origin[0] and (x < cv.endpoint[0]):
        if y > cv.origin[1] and (y < cv.endpoint[1]):
            return 0  # everything is okay
    return 1


def get_stroke_endpoint(cv, art_direction, startX, startY, specific=""):
    """ Returns endX and endY points per directives

        if StartX and startY are specified, they will be used
        Length plays an important role. It should be specified inside art_direction
        Length can be completely 'random' or,
        Length can be {'Long', 'Med|ium' or 'short} or,
        Length can be an exact number of pixels or,
        Length can be a range (between (min, max)).
        Angle & length if specified will be used
    """
    safety = 0
    foundx, foundy = 0, 0

    if is_pt_outside_canvas(cv, startX, startY):
        print(f"Error. Starting point is outside the canvas {startX} {startY}")
        print(cv)
        sys.exit(1)

    llen = art_direction["LINE_LENGTH"]["line_length"]
    angles = art_direction["LINE_LENGTH"]["angles"]

    while not (foundx and foundy):
        safety += 1

        if safety > 100:
            return cv.center  # give up and start from center

        if "random" in llen:
            stroke_len_x = random.randint(0, cv.width)
            stroke_len_y = random.randint(0, cv.height)
            if not foundx:
                end_x = random.choice([startX - stroke_len_x, startX + stroke_len_x])
            if not foundy:
                end_y = random.choice([startY - stroke_len_y, startY + stroke_len_y])

        if "random" in angles:
            theta = math.radians(
                random.randint(-180, 180)
            )  # in radians, converted from degrees
        else:
            theta = math.radians(int(random.choice(angles)))

        if llen[0].isnumeric():
            stroke_len = int(llen[0])
            if not foundx:
                DIRX = random.choice([1, -1])
                end_x = startX + (int(stroke_len * math.cos(theta)) * DIRX)
            if not foundy:
                DIRY = random.choice([1, -1])
                end_y = startY + (int(stroke_len * math.sin(theta)) * DIRY)
            # minus_x = startX - int(stroke_len * math.cos(theta))
            # minus_y = startY - int(stroke_len * math.sin(theta))

        if not foundx:
            if (end_x < cv.endpoint[0]) and (end_x > cv.origin[0]):
                foundx = True

        if not foundy:
            if (end_y < cv.endpoint[1]) and (end_y > cv.origin[1]):
                foundy = True

        if safety > 50:
            print("unable to find endx, endy")
            print(f"{startX} {startY} Angles {angles} Len {llen}")
            print(f"theta {math.cos(theta)} stroke {stroke_len}")
            print(f"theta {math.sin(theta)} stroke {stroke_len}")
            print(cv)


    print(
        f"st {startX} {startY} {end_x} {end_y} cv {cv.origin} {cv.endpoint} foundx {foundx} foundy {foundy} {safety}"
    )
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
