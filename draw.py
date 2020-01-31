import math
import random
import sys

import pyautogui as pg

from utils import *


def get_start_pt(cv, art_direction, specific=""):
    """Return X Y coords per art_direction directives specified"""

    # by default, assume Random starting point
    startX = random.randint(cv.origin[0], cv.endpoint[0])
    startY = random.randint(cv.origin[1], cv.endpoint[1])
    print(f"starting at {startX} {startY}")

    return startX, startY


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

    if is_pt_outside_canvas(cv, startX, startY):
        print(f"Error. Starting point is outside the canvas {startX} {startY}")
        print(cv)
        sys.exit(1)

    llen = art_direction["LINE_LENGTH"]["line_length"]

    if "angles" in art_direction["LINE_LENGTH"]:
        angles = art_direction["LINE_LENGTH"]["angles"]

    foundx, foundy = 0, 0
    while not (foundx and foundy):
        safety += 1

        if safety > 100:
            return cv.center  # give up and start from center

        if "random" in angles or "None" in angles:
            theta = math.radians(
                random.randint(-180, 180)
            )  # in radians, converted from degrees
            # print(f"theta {theta}")
        else:
            theta = math.radians(int(random.choice(angles)))

        if "random" in llen:
            if "None" in angles:
                stroke_len_x = random.randint(0, cv.width)
                stroke_len_y = random.randint(0, cv.height)
                if not foundx:
                    end_x = random.choice(
                        [startX - stroke_len_x, startX + stroke_len_x]
                    )
                if not foundy:
                    end_y = random.choice(
                        [startY - stroke_len_y, startY + stroke_len_y]
                    )
                if not foundx:
                    if (end_x < cv.endpoint[0]) and (end_x > cv.origin[0]):
                        foundx = True
                if not foundy:
                    if (end_y < cv.endpoint[1]) and (end_y > cv.origin[1]):
                        foundy = True

        if "random" in llen:
            stroke_len = random.randint(0, cv.width)
        if "short" in llen:
            stroke_len = random.randint(0, int(cv.width / 4))
        if "medium" in llen:
            stroke_len = random.randint(int(cv.width / 4), int(cv.width / 2))
        if "long" in llen:
            stroke_len = random.randint(int(cv.width * 0.6), int(cv.width) * 0.95)
        if llen[0].isnumeric():  # exact length given
            stroke_len = int(llen[0])

        if not foundx:
            DIRX = random.choice([1, -1])
            end_x = startX + (int(stroke_len * math.cos(theta)) * DIRX)
        if not foundy:
            DIRY = random.choice([1, -1])
            end_y = startY + (int(stroke_len * math.sin(theta)) * DIRY)

        if not foundx:
            if (end_x < cv.endpoint[0]) and (end_x > cv.origin[0]):
                foundx = True

        if not foundy:
            if (end_y < cv.endpoint[1]) and (end_y > cv.origin[1]):
                foundy = True

        if not (foundx and foundy):  # both are not okay
            foundx, foundy = False, False

        if safety > 50:
            print("unable to find endx, endy safely")
            print(f"{startX} {startY} Angles {angles} Len {llen}")
            print(f"theta {math.cos(theta)} stroke {stroke_len}")
            print(f"theta {math.sin(theta)} stroke {stroke_len}")
            print(cv)

    print(
        f"from {startX} {startY} to {end_x} {end_y} | cv {cv.origin} {cv.endpoint}  {safety}"
    )
    return (end_x, end_y)


def draw_borders(msp, cv):

    print("borders")
    print(
        (cv.endpoint[0] - 50, cv.origin[1] + 50),
        (cv.endpoint[0] - 50, cv.endpoint[1] - 50),
    )
    print(
        (cv.origin[0] + 800, cv.origin[1] + 5), (cv.origin[0] + 800, cv.endpoint[1] - 5)
    )
    cv.draw_line(
        msp,
        (cv.endpoint[0] - 5, cv.origin[1] + 5),
        (cv.endpoint[0] - 5, cv.endpoint[1] - 5),
        color="gold",
    )
    cv.draw_line(
        msp,
        (cv.origin[0] + 5, cv.origin[1] + 5),
        (cv.origin[0] + 5, cv.endpoint[1] - 5),
        color="red",
    )
    cv.draw_line(
        msp,
        (cv.origin[0] + 5, cv.origin[1] + 5),
        (cv.endpoint[0] - 5, cv.origin[1] + 5),
        color="black",
    )
    cv.draw_line(
        msp,
        (cv.origin[0] + 5, cv.endpoint[1] - 5),
        (cv.endpoint[0] - 5, cv.endpoint[1] - 5),
        color="blue",
    )
