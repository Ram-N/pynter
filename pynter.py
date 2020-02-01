import configparser
import json
import math
import random
import sys

import pyautogui as pg

from utils import *
from draw import *
from msp import *

"""
Ram Narasimhan
Pynter is derived from: Doodlrr by Eric Hamilton erickenneth91@gmail.com
"""


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.origin = (861, 228)
        self.endpoint = (1761, 732)
        self.center = (1311.0, 480.0)

    def __str__(self):
        return f" Canvas object: {self.width} by {self.height} \
                \n Origin = {self.origin}\
                \n End = {self.endpoint}   \
                \n Center =  {self.center}\n"

    def manually_calibrate_canvas(self):
        print("CALIBRATING ORIGIN POINT of CANVAS:")
        print("Hold your cursor at the TOP LEFT corner of the image canvas")
        wait_loop(WAIT_SECONDS)
        self.origin = pg.position()
        self.endpoint = (self.origin[0] + self.width, self.origin[1] + self.height)

        self.center = (
            (self.width / 2) + self.origin[0],
            (self.height / 2) + self.origin[1],
        )
        print(f"Canvas origin {self.origin}")
        print(f"center {self.center}")
        print(f"Canvas End {self.endpoint}")

    def draw_line(
        self, msp, st, end, color="", brush_size="", brush_style="", color_index={}
    ):
        """ Draws a line from startxy to endxy, with specified items.

        st to end, using the color/size/brush type. If any of these are 
        not specified, just the default that it came with is used to draw
        the straight line.

        Parameters
        ----------
        st: tuple 
            The coordinates of the starting point
        end: tuple 
            The coordinates of the end point
        color : str
            One of the colors in ALL_COLORS
        brush_size : str
            One of the colors in BRUSH_SIZES
        brush_style : str
            One of the brushes in in BRUSH_STYLES
        """

        if color != "":
            msp.pick_item("color", selected=color, palette=color_index)
        if brush_size != "":
            msp.pick_item("brush_size", selected=brush_size)
        if brush_style != "":
            msp.pick_item("brush_style", selected=brush_style)

        start_x, start_y = st[0], st[1]
        end_x, end_y = end[0], end[1]
        # print(start_x, start_y, end_x, end_y)
        pg.moveTo(start_x, start_y)
        pg.dragTo(end_x, end_y, button="left")
        return

    def draw(self, msp, art_direction, num_strokes=10):
        """This is the main function where the painting happens.

        Args:
            num_strokes: Number of brushstrokes to make

        Returns:
            None. Just defaults to rendering the menu

        """
        color_change = False
        continuous_flag = False
        size_change = True
        brush_change = True

        for k, vlist in art_direction.items():

            if k == "NUM_STROKES":
                num_strokes = int(art_direction["NUM_STROKES"][0])

            if k == "COLOR_SEQUENCE":
                for v in vlist:
                    if v == "random":
                        color_change = True

            if k == "PALETTE":
                palette = get_color_index_dict(vlist)
                if len(vlist) == 1:
                    color_change = False

            if k == 'BRUSHES':
                if len(vlist) == 1:
                    brush_change = False

            if k == 'BRUSH-SIZES':
                if len(vlist) == 1:
                    size_change = False


        if "continuous" in art_direction["START_POINTS"]:
            continuous_flag = True
            endX, endY = get_start_pt(self, art_direction, specific="random")

        active_brushes = get_active_brushes(art_direction)
        active_sizes = get_active_sizes(art_direction)
        thresholds = get_thresholds(art_direction)

        print(f'Active Sizes {active_sizes}')
        print(f'thresholds {thresholds}')
        print(f'color_change={color_change} size change {size_change}, brush change {brush_change}')

        #initialize Color, Size and Brush
        msp.pick_item(item_type="color", selected="", palette=palette)
        msp.pick_item(item_type="brush_size", selected="", sizes=active_sizes)
        msp.pick_item(
            item_type="brush_style", selected="", brushes=active_brushes
        )

        for stroke in range(num_strokes):

            if color_change and ('color_change' in thresholds):
                if random.randint(0, 100) > thresholds['color_change']:
                    msp.pick_item(item_type="color", selected="", palette=palette)

            if size_change and ('size_change' in thresholds):
                if random.randint(0, 100) > thresholds['size_change']:
                    msp.pick_item(item_type="brush_size", selected="", sizes=active_sizes)

            if brush_change and ('brush_change' in thresholds):
                if random.randint(0, 100) > thresholds['brush_change']:
                    msp.pick_item(
                        item_type="brush_style", selected="", brushes=active_brushes
                    )

            # if random.randint(0,100) > 75:
            #    curve()
            if continuous_flag:
                startX, startY = endX, endY
            else:
                startX, startY = get_start_pt(self, art_direction, specific="random")

            pg.moveTo(startX, startY)
            endX, endY = get_stroke_endpoint(self, art_direction, startX, startY)
            self.draw_line(msp, (startX, startY), (endX, endY))

            # pg.dragTo(end_x, end_y, button="left")  # this is where the line gets drawn
            if stroke % 10 == 0:
                print(f"stroke # {stroke} {startX} {startY} {endX} {endY}")


def curve(cv):
    startX = random.randint(cv.origin[0], cv.origin[2])
    startY = random.randint(cv.origin[1], cv.origin[3])
    endX = random.randint(cv.origin[0], cv.origin[2])
    endY = random.randint(cv.origin[1], cv.origin[3])

    pg.moveTo(startX, startY)
    dist = abs(endX - startX)
    for _ in range(dist):
        current = pg.position()
        currX = current[0]
        currY = current[1]
        if endX > startX:
            newX = currX + 1
        if endX < startX:
            newX = currX - 1
        newY = cv.center[1] + math.tan(newX)  # *(random.randint(2, height/2))
        pg.dragTo(newX, newY)


def recaliberate(cv, CANVAS_VARIABLE=False):

    print("Be sure you can see your print output during this process.")

    if CANVAS_VARIABLE:
        print("What is the width of the Canvas in pixels?")
        pixW = input()
        cv.width = int(pixW)
        print("What is the height of the Canvas in pixels?")
        pixH = input()
        cv.height = int(pixH)
        print("OK, now to get screen coordinates of certain features in Paint.")
        # print("press Enter")
        # input()
        print("How long do you need to get your cursor in place? (seconds)")
        wait_time = int(input())

    # manually_calibrate_size here

    # manually calibrate Origin Point here

    return cv


def display_menu(msp, cv, art_direction, SPECIFY_NUM_TICKS):

    print("\nEnter (Type) an option and Press Enter:")
    print(
        "1: Draw (b)orders 2: Get Cursor Coords 3: Recalibrate Coords \t \
            4: 4 corners of the Canvas"
    )
    print("5: \t Print Canvas and MSP Coords \t 6. Show Size and Brush-type Btns")
    print("7pc. Print all colors \t 7pb. Print all Brushes \t 7ps. Print all Sizes")
    print("8cc. Click all colors \t 8cb. Click all Brushes \t 8cs. Click all Sizes")
    print("9dc. Draw all colors \t 9db. Draw all Brushes \t\t 9ds. Draw all Sizes")

    result = input()

    if "1" in result:
        print("Press ctrl alt del to abort")
        ticks = 100
        if SPECIFY_NUM_TICKS:
            ticks = input()
        wait_loop(WAIT_SECONDS)
        if "b" in result:
            draw_borders(msp, cv)
        cv.draw(msp, art_direction, int(ticks))
        display_menu(msp, cv, art_direction, SPECIFY_NUM_TICKS=False)

    if result == "2":
        print("For how long? (secs)")
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

    config = configparser.ConfigParser()
    config.read("config/art_direction.cfg")

    art_direction = as_dict(config)

    for section in config.sections():
        for key in config[section]:
            _list = config[section][key]
            DIRS = [e.strip() for e in _list.split(",")]
            if len(config[section]) > 1:
                art_direction[section][key] = DIRS  # nested
            else:
                art_direction[section] = DIRS

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
        cv = display_menu(msp, cv, art_direction, SPECIFY_NUM_TICKS=False)


# These should all eventually come either from cfg file or cmdline args
SPECIFY_NUM_TICKS = False
NUM_TICKS = 100
COLOR_CHANGE_THRESHOLD = 80
SIZE_CHANGE_THRESHOLD = 95
# BRUSH_CHANGE_THRESHOLD = 90
STYLE_CHANGE_THRESHOLD = 97
STYLE_CHANGE = True
COLOR_CHANGE = True
SIZE_CHANGE = True

MAX_STROKE_LEN = 30
MIN_STROKE_LEN = 5

# PALETTE = ALL_COLORS


if __name__ == "__main__":
    main()

