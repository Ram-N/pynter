import json
import math
import random
import sys

import pyautogui as pg

from utils import *
from draw import *
from msp import *
from canvas import *

"""
Ram Narasimhan
Pynter is derived from: Doodlrr by Eric Hamilton erickenneth91@gmail.com
"""


def display_menu(msp, cv, art_direction):

    print("\nEnter (Type) an option and Press Enter:")
    print(
        "1: Draw (b)orders 2: Re-read Art Directives cc: Get Cursor Coords 3: Recalibrate Coords \
            4: 4 corners of the Canvas"
    )
    print("5: \t Print Canvas, MSP, & Art Dir  \t 6. Show Size and Brush-type Btns")
    print("7pc. Print all colors \t 7pb. Print all Brushes \t 7ps. Print all Sizes")
    print("8cc. Click all colors \t 8cb. Click all Brushes \t 8cs. Click all Sizes")
    print("9dc. Draw all colors \t 9db. Draw all Brushes \t\t 9ds. Draw all Sizes")

    result = input()

    if "1" in result:
        print("Press ctrl alt del to abort")
        ticks = 100
        wait_loop(WAIT_SECONDS)
        if "b" in result:
            draw_borders(msp, cv)
        cv.draw(msp, art_direction, int(ticks))
        display_menu(msp, cv, art_direction)

    if result == "2":
        art_direction = read_art_directives()  # utils
        print(art_direction)

    if result == "cc":
        print("Get Cursor Coords \n For how long? (secs)")
        secs = input()
        get_coords(int(secs))
    if result == "3":
        cv = recaliberate(cv, CANVAS_VARIABLE=False)
    if result == "4":
        wait_loop(WAIT_SECONDS)
        draw_borders(msp, cv)
        # get_4_points(5)
    if result == "5":
        print(cv)
        print(msp)
        print(art_direction)

    if result == "6":  # show size and Style buttons
        wait_loop(WAIT_SECONDS)
        pg.moveTo(msp.brush_size_btn)
        time.sleep(0.5)

        pg.moveTo(msp.brush_style_btn)
        time.sleep(0.5)
        pg.click()
        time.sleep(0.5)
        msp.pick_item(item_type="brush_style", selected="")

    test_d = {
        "7pb": ("print", "brush_style"),
        "7pc": ("print", "color"),
        "7ps": ("print", "brush_size"),
        "8cc": ("click", "color"),
        "8cb": ("click", "brush_style"),
        "8cs": ("click", "brush_size"),
        "9dc": ("draw", "color"),
        "9ds": ("draw", "brush_size"),
        "9db": ("draw", "brush_style"),
    }
    if result in test_d:
        action, item_type = test_d[result][0], test_d[result][1]
        if action != "print":
            wait_loop(WAIT_SECONDS)
        msp.test_all_items(cv, action, item_type, art_direction)

    if result == "x":
        sys.exit()

    return cv


def main():

    art_direction = read_art_directives()  # utils

    cv = Canvas(900, 504)
    msp = MSPaint(5, MANUAL_COLOR=False, MANUAL_SIZE=False)

    if is_invalid(art_direction, cv):
        print("Invalid directions \n Please fix and rerun")
        sys.exit(1)

    # msp.pick_color("orange")
    # msp.click()
    # cv.draw_line((1200, 500), (1400, 500))
    # cv.manually_calibrate_canvas()
    msp.display_all_sizes()
    # msp.manually_calibrate("Brushes")
    print("Art Direction")
    print(art_direction)
    if VERBOSE:
        print(cv)
        print(msp)
    # cv = recaliberate(cv, CANVAS_VARIABLE=False)

    while True:
        cv = display_menu(msp, cv, art_direction)


# These should all eventually come either from cfg file or cmdline args
# COLOR_CHANGE_THRESHOLD = 80
# SIZE_CHANGE_THRESHOLD = 95
# BRUSH_CHANGE_THRESHOLD = 90
# STYLE_CHANGE_THRESHOLD = 97
# STYLE_CHANGE = True
# COLOR_CHANGE = True
# SIZE_CHANGE = True

# MAX_STROKE_LEN = 30
# MIN_STROKE_LEN = 5

# PALETTE = ALL_COLORS


if __name__ == "__main__":
    main()

