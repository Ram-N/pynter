import configparser
import json
import math
import random
import sys

import pyautogui as pg

from utils import *
from draw import *


"""
Ram Narasimhan
Pynter is derived from: Doodlrr by Eric Hamilton erickenneth91@gmail.com
"""


BRUSH_STYLES = {
    "brush": (1, 1),
    "callig brush1": (1, 2),
    "callig brush2": (1, 3),
    "Airbrush": (1, 4),
    "oil": (2, 1),
    "crayon": (2, 2),
    "marker": (2, 3),
    "pencil": (2, 4),
    "watercolor": (3, 1),
}

BRUSH_SIZES = {"8px": 0, "16px": 1, "30px": 2, "40px": 3}


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
        random_colors = False
        continuous_flag = False
        startX, startY = self.origin[0], self.origin[1]

        for k, vlist in art_direction.items():

            if k == "NUM_STROKES":
                num_strokes = int(art_direction["NUM_STROKES"][0])

            if k == "PALETTE":
                palette = get_color_index_dict(vlist)

            if k == "COLOR_SEQUENCE":
                for v in vlist:
                    if v == "random":
                        random_colors = True

        if "continuous" in art_direction["START_POINTS"]:
            continuous_flag = True
            endX, endY = get_start_pt(self, art_direction, specific="random")

        for stroke in range(num_strokes):

            if random_colors:
                if random.randint(0, 100) > COLOR_CHANGE_THRESHOLD:
                    msp.pick_item(item_type="color", selected="", palette=palette)

            if random.randint(0, 100) > SIZE_CHANGE_THRESHOLD:
                msp.pick_item(item_type="brush_size", selected="")

            if random.randint(0, 100) > STYLE_CHANGE_THRESHOLD:
                msp.pick_item(item_type="brush_style", selected="")

            # if random.randint(0,100) > 75:
            #    curve()
            if continuous_flag:
                startX, startY = endX, endY

            pg.moveTo(startX, startY)
            endX, endY = get_stroke_endpoint(self, art_direction, startX, startY)
            self.draw_line(msp, (startX, startY), (endX, endY))

            # pg.dragTo(end_x, end_y, button="left")  # this is where the line gets drawn
            if stroke % 1 == 0:
                print(f'stroke {stroke} {startX} {startY} {endX} {endY}')


class MSPaint:
    def __init__(self, wait, MANUAL_COLOR=False, MANUAL_SIZE=False):

        self.wait = 5  # Seconds to wait
        self.swatch_top_left = (1430, 95)
        self.swatch_bottom_right = (1723, 141)
        self.swatch_offset = (32, 46)
        self.brush_size_btn = (1239, 125)
        self.brush_style_btn = (1099, 175)
        self.style_TR = (1098, 218)
        self.style_LL = (923, 324)
        self.brush_style_offset = (63, 59)
        self.size_options = (217, 261, 310, 392)

        if MANUAL_COLOR:
            self.manually_calibrate_colors()
        if MANUAL_SIZE:
            self.manually_calibrate_size()

        self.calculate_offset("brush_style")

    def __str__(self):
        return f" MS Paint object: \n COLOR TL {self.swatch_top_left} \
            \n COLOR BR = {self.swatch_bottom_right} \
            \n Color offset = {self.swatch_offset}  \
            \n Size Btn =  {self.brush_size_btn} \
            \n Size Options =  {self.size_options} \
            \n Style Btn = {self.brush_style_btn} \
            \n Style TR {self.style_TR}, Style LL {self.style_LL}"

    def manually_calibrate(self, btn_name):
        pretext = f"Move cursor to {btn_name}"
        posttext = f"Captured {btn_name}\n"
        btn_pos = capture_coords(btn_name, pretext, posttext)

        if btn_name == "Brushes":
            self.brush_style_btn = btn_pos
            self.style_LL = capture_coords(
                btn_name, "Move to the lower left (watercolor) brush", "captured\n"
            )
            self.style_TR = capture_coords(
                btn_name, "Move to the upper right (Airbrush) button", "captured\n"
            )

            self.calculate_offset("brush_style")

    def calculate_offset(self, item_type):

        if item_type == "brush_style":
            NUM_ROWS, NUM_COLS = 3, 4
            offsetX = (self.style_TR[0] - self.style_LL[0]) / (NUM_COLS - 1)
            offsetY = (self.style_LL[1] - self.style_TR[1]) / (NUM_ROWS - 1)
            self.brush_style_offset = (int(offsetX), int(offsetY))
            print(f"Brush Button Offset X, Y is {self.brush_style_offset}")

    def manually_calibrate_colors(self):
        print("Move Cursor to the top left color swatch in Paint")
        wait_loop(self.wait)
        pos1 = pg.position()
        print(f"Captured TL {pos1}")
        print("Now move your cursor to the bottom right color swatch in Paint")
        wait_loop(self.wait)
        pos2 = pg.position()
        self.swatch_top_left = pos1
        self.swatch_bottom_right = pos2
        print(f"Captured BR {pos2}")
        offsetX = (pos2[0] - pos1[0]) / (NUM_COLOR_BUTTONS[0] - 1)
        offsetY = pos2[1] - pos1[1]
        self.swatch_offset = (offsetX, offsetY)
        print(f"Color Button Offset {self.swatch_offset}")

    def manually_calibrate_size(self):
        btn = "Brush-size-selector"
        pretext = "CALIBRATING BRUSH SIZES \n Move your cursor to the Brush Size Button"
        posttext = "Captured" + " " + btn
        self.brush_size_btn = capture_coords(btn, pretext, posttext)

        pretext = "Move the cursor to the smallest brush size option\n \
            First Click the size selection Button, then move to the smallest thickness"
        posttext = "Captured Small Brush\n\n"
        small_pos = capture_coords(btn, pretext, posttext)

        pretext = "Move the cursor to the biggest brush size option\n \
            First Click the size selection Button, then move to the biggest thickness"
        posttext = "Captured Biggest Brush Coords\n\n"
        big_pos = capture_coords(btn, pretext, posttext)

        small_y = small_pos[1]
        big_y = big_pos[1]
        brush_step = (big_y - small_y) / NUM_BRUSH_SIZES
        self.size_options = (
            small_y,
            small_y + brush_step,
            small_y + (brush_step * 2),
            big_y,
        )
        print(f"Brushes between: {big_pos}, {small_pos}")

    def get_selected_items_coords(self, item_type, selected, palette={}):
        """ 
        Returns the X,Y coords of any selected item on Paint App
        
        Parameters
        ----------
        item_type : str
            The MS Paint item. One of {'color', 'brush_style'}
        selected : str
            The color or brush_style whose coords are needed
            One of {PALETTE.keys() or BRUSH_STYLE.keys()}
        """
        if item_type == "color":
            (btn_idx_x, btn_idx_y) = palette.get(selected)
            x = self.swatch_top_left[0] + (btn_idx_x - 1) * self.swatch_offset[0]
            y = self.swatch_top_left[1] + (btn_idx_y - 1) * self.swatch_offset[1]
            return (x, y)

        if item_type == "brush_style":
            (btn_idx_y, btn_idx_x) = BRUSH_STYLES.get(selected)
            x = self.style_LL[0] + (btn_idx_x - 1) * self.brush_style_offset[0]
            y = self.style_TR[1] + (btn_idx_y - 1) * self.brush_style_offset[1]
            return (x, y)

    def pick_item(self, item_type="color", selected="", palette={}):

        if item_type == "color":
            if selected == "":
                color = random.choice(list(palette.keys()))
            else:
                color = selected
                palette = get_color_index_dict([color])
                print(color)
                if VERBOSE:
                    print(color)

            print(palette)

            color_xy = self.get_selected_items_coords(item_type, color, palette=palette)
            # print(f"{color} @ {color_xy}")
            pg.moveTo(color_xy)
            time.sleep(0.5)
            pg.click(color_xy)  # select the color

        if item_type == "brush_size":
            pg.moveTo(self.brush_size_btn)
            pg.click()

            if selected == "":
                brush_size_y = random.choice(self.size_options)
            else:
                b_index = BRUSH_SIZES[selected]
                brush_size_y = self.size_options[b_index]

            pg.moveTo(self.brush_size_btn[0], brush_size_y)
            time.sleep(0.25)
            pg.click()
            if VERBOSE:
                print(f"Size {brush_size_y}, size_position {self.brush_size_btn}")

        if item_type == "brush_style":
            pg.moveTo(self.brush_style_btn)
            pg.click()
            time.sleep(0.8)

            if selected == "":
                style = random.choice(list(BRUSH_STYLES.keys()))
            else:
                style = selected

            pos_xy = self.get_selected_items_coords(item_type, style)
            if VERBOSE:
                print(f"{item_type} {style} @ {pos_xy}")
            pg.moveTo(pos_xy)
            time.sleep(0.8)
            pg.click(pos_xy)  # select the indiv item

    def test_all_items(
        self, cv, action_type="print", item_type="color", art_direction={}
    ):
        """ 
        This is a debugging and re-calibrating method.

        There are 3 things that this function can do.
        Print the coords on the screen,CLICK each item, or
        DRAW with each item. (This requires calculating coords)

        Parameters
        ----------
        action_type : str
            One of {'print', 'click', 'draw'}. 'print' will display all the releated 
            coords in the terminal. 'click' will sequentially click each button in the item_type.
            'draw' will actually use the tool of interest and render it on the canvas. 
        item_type : str
            The MS Paint item. One of {'color', 'brush_style', 'brush_size'}
        """
        if action_type == "click":
            if item_type == "brush_style":
                for k, _ in BRUSH_STYLES.items():
                    self.pick_item(item_type, selected=k)

            if item_type == "color":
                palette_d = get_color_index_dict(
                    art_direction["PALETTE"]
                )  # arg should be a valid list of colors
                for k, _ in palette_d.items():
                    self.pick_item(item_type, selected=k, palette=palette_d)

            if item_type == "brush_size":
                for k, _ in BRUSH_SIZES.items():
                    self.pick_item(item_type, selected=k)

        elif action_type == "print":
            if item_type == "color":
                palette_d = get_color_index_dict(
                    art_direction["PALETTE"]
                )  # arg should be a valid list of colors
                for k, _ in palette_d.items():
                    print(
                        k, "\t", self.get_selected_items_coords("color", k, palette_d)
                    )
            if item_type == "brush_style":
                for k, _ in BRUSH_STYLES.items():
                    print(k, "\t", self.get_selected_items_coords("brush_style", k))

            if item_type == "brush_size":
                for k, _ in BRUSH_SIZES.items():
                    print(
                        k,
                        "\t (",
                        self.brush_size_btn[0],
                        self.size_options[BRUSH_SIZES[k]],
                        ")",
                    )

        elif action_type == "draw":
            if item_type == "color":
                palette_d = get_color_index_dict(
                    art_direction["PALETTE"]
                )  # arg should be a valid list of colors

                for i, k in enumerate(palette_d):
                    stx = cv.origin[0] + 10
                    sty = cv.origin[1] + 10 * (i + 1)
                    cv.draw_line(
                        self, (stx, sty), (stx + 50, sty), color=k, palette=palette_d
                    )
            elif item_type == "brush_size":
                for i, k in enumerate(BRUSH_SIZES):
                    stx = cv.origin[0] + 70
                    sty = cv.origin[1] + 10 * (i + 1)
                    cv.draw_line(self, (stx, sty), (stx + 50, sty), brush_size=k)
            elif item_type == "brush_style":
                for i, k in enumerate(BRUSH_STYLES):
                    stx = cv.origin[0] + 110
                    sty = cv.origin[1] + 40 * (i + 1)
                    cv.draw_line(self, (stx, sty), (stx + 50, sty), brush_style=k)

        else:
            return

    def click(self):
        pg.click()

    def print_all_colors(self):

        print(f"swatch top left {self.swatch_top_left}")
        print(f"swatch offset {self.swatch_offset}")
        for c, ci in ALL_COLORS.items():
            print(f"{c}, {ci}, {self.get_selected_items_coords('color', c)}")

    def display_all_sizes(self):
        print(f"Size options are {self.size_options}")
        print(f"size_Button is @ {self.brush_size_btn}")



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
        "1: Draw (b)orders 2: Get Cursor Coords 3: Recalibrate Coords \
            \t 4: 4 corners of the Canvas"
    )
    print("5: Print Canvas and MSP Coords \t 6. Show Size and Brush-type Btns")
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
        if 'b' in result:
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
        #get_4_points(5)
    if result == "5":
        print(cv)
        print(msp)
    if result == "6":
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
    config.read("art_direction.cfg")

    art_direction = {
        "line-length": "end-to-end",
        "everything": "all-random",
        "colors": "random",
        "palette": BLACK_WHITE,
    }

    art_direction = as_dict(config)

    for section in config.sections():
        for key in config[section]:
            _list = config[section][key]
            DIRS = [e.strip() for e in _list.split(",")]
            if len(config[section]) > 1:
                art_direction[section][key] = DIRS #nested
            else:
                art_direction[section] = DIRS

    cv = Canvas(900, 504)
    msp = MSPaint(5, MANUAL_COLOR=False, MANUAL_SIZE=False)

    if is_invalid(art_direction, cv):
        print('Invalid directions \n Please fix and rerun')
        sys.exit(1)

    # msp.pick_color("orange")
    # msp.click()
    # cv.draw_line((1200, 500), (1400, 500))
    # cv.manually_calibrate_canvas()
    msp.display_all_sizes()
    # msp.manually_calibrate("Brushes")
    print('Art Direction')
    print(art_direction)

    if VERBOSE:
        print(cv)
        print(msp)
    # cv = recaliberate(cv, CANVAS_VARIABLE=False)


    while True:
        cv = display_menu(msp, cv, art_direction, SPECIFY_NUM_TICKS=False)


# These should all eventually come either from cfg file or cmdline args
VERBOSE = False
SPECIFY_NUM_TICKS = False
NUM_TICKS = 100
NUM_COLOR_BUTTONS = (10, 2)
NUM_BRUSH_SIZES = 4
COLOR_CHANGE_THRESHOLD = 95
SIZE_CHANGE_THRESHOLD = 95
BRUSH_CHANGE_THRESHOLD = 90
STYLE_CHANGE_THRESHOLD = 97
STYLE_CHANGE = True
COLOR_CHANGE = True
SIZE_CHANGE = True

MAX_STROKE_LEN = 30
MIN_STROKE_LEN = 5

# PALETTE = ALL_COLORS
JAMAICAN_COLORS = ["yellow", "green", "black"]
BLACK_WHITE = ["white", "gray25", "gray50", "black"]


if __name__ == "__main__":
    main()

