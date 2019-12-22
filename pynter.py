import random
import time
import math
import sys

import pyautogui as pg


"""
Ram Narasimhan
Pynter is derived from: Doodlrr by Eric Hamilton erickenneth91@gmail.com
"""


class Canvas:
    def __init__(self, width, height, MANUAL_CANVAS=False):
        self.width = width
        self.height = height
        self.origin = (861, 228)
        self.endpoint = (1761, 732)
        self.center = (1311.0, 480.0)

        if MANUAL_CANVAS:
            self.manually_calibrate_canvas()

    def manually_calibrate_canvas(self):
        print("CALIBRATING ORIGIN POINT of CANVAS:")
        print("Hold your cursor at the TOP LEFT corner of the image canvas")
        print("Get it as close as possible")
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

    def draw_line(self, st, end):
        start_x, start_y = st[0], st[1]
        end_x, end_y = end[0], end[1]
        # print(start_x, start_y, end_x, end_y)
        pg.moveTo(start_x, start_y)
        pg.dragTo(end_x, end_y, button="left")
        return

    def get_stroke_endpoint(self):

        pos = pg.position()
        startX = pos[0]
        startY = pos[1]
        stroke_len = random.randint(2, 30)  # PARAMETRIZE

        found = 0
        while not found:
            end_x = random.randint(
                startX - int((self.width / stroke_len)),
                startX + int((self.width / stroke_len)),
            )
            end_y = random.randint(
                startY - int((self.height / stroke_len)),
                startY + int((self.height / stroke_len)),
            )
            if end_x > self.endpoint[0]:
                continue
            elif end_x < self.origin[0]:
                continue
            elif end_y > self.endpoint[1]:
                continue
            elif end_y < self.origin[1]:
                continue
            else:
                # print(f'new move coords {end_x} {end_y}')
                return (end_x, end_y)

    def draw(self, msp, num_strokes):
        """This is the main function where the painting happens.

        Args:
            num_strokes: Number of brushstrokes to make

        Returns:
            None. Just defailts to rendering the menu

        """
        for stroke in range(num_strokes):
            if random.randint(0, 100) > ONE_IN_10:
                msp.pick_color()
            if random.randint(0, 100) > ONE_IN_20:
                msp.pick_size()
            # if random.randint(0,100) > 75:
            #    curve()
            startX = random.randint(self.origin[0], self.endpoint[0])
            startY = random.randint(self.origin[1], self.endpoint[1])
            pg.moveTo(startX, startY)
            end_x, end_y = self.get_stroke_endpoint()
            self.draw_line((startX, startY), (end_x, end_y))
            # pg.dragTo(end_x, end_y, button="left")  # this is where the line gets drawn
            if stroke % 10 == 0:
                print(stroke)


class MSPaint:
    def __init__(self, wait, MANUAL_COLOR=False, MANUAL_SIZE=False):

        self.wait = 5  # Seconds to wait
        self.swatch_top_left = (1430, 95)
        self.swatch_bottom_right = (1723, 141)
        self.swatch_offset = (32, 46)
        self.brush_size_btn = (1239, 125)
        self.size_options = (217, 261, 310, 392)

        if MANUAL_COLOR:
            self.manually_calibrate_colors()
        if MANUAL_SIZE:
            self.manually_calibrate_size()

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
        print("CALIBRATING BRUSH SIZES")
        print("Move your cursor to the Brush Size Button")
        wait_loop(self.wait)
        self.brush_size_btn = pg.position()
        print("Captured")

        print("Move the cursor to the smallest brush size option")
        print(
            "First Click the size selection Button, then move to the smallest thickness"
        )
        wait_loop(self.wait)
        small_pos = pg.position()
        print(f"Captured Small Brush @ {small_pos}")

        print("Move the cursor to the largest brush size option")
        wait_loop(self.wait)
        big_pos = pg.position()
        print(f"Captured Largest Brush @ {big_pos}")

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

    def color_button_coords(self, color):
        """ returns the X,Y coords of any selected Color on Paint App"""
        (btn_idx_x, btn_idx_y) = PALETTE.get(color)
        x = self.swatch_top_left[0] + (btn_idx_x - 1) * self.swatch_offset[0]
        y = self.swatch_top_left[1] + (btn_idx_y - 1) * self.swatch_offset[1]
        return (x, y)

    def pick_color(self, color=""):

        if color == "":
            color = random.choice(list(PALETTE.keys()))
        color_xy = self.color_button_coords(color)
        print(f"{color} @ {color_xy}")
        pg.moveTo(color_xy)
        time.sleep(0.5)
        pg.click(color_xy)  # select the color

    def click(self):
        pg.click()

    def print_all_colors(self):

        print(f"swatch top left {self.swatch_top_left}")
        print(f"swatch offset {self.swatch_offset}")
        for c, ci in PALETTE.items():
            print(f"{c}, {ci}, {self.color_button_coords(c)}")

    def pick_size(self, brush_size_y=""):

        pg.moveTo(self.brush_size_btn)
        pg.click()

        if brush_size_y == "":
            brush_size_y = random.choice(self.size_options)

        pg.moveTo(self.brush_size_btn[0], brush_size_y)
        time.sleep(0.25)
        pg.click()
        if VERBOSE:
            print(f"SELECTED size {brush_size_y}, size_position {self.brush_size_btn}")

    def display_all_sizes(self):
        print(f"Size options are {self.size_options}")
        print(f"size_Button is @ {self.brush_size_btn}")


def wait_loop(wait_time):
    print("Press Enter to start countdown")
    input()
    count = wait_time
    while count > 0:
        print(str(count) + "...", end=" ", flush=True)
        time.sleep(1)
        count -= 1


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


def get_4_points(wait_time=5):

    for _ in range(4):
        wait_loop(wait_time)
        print(pg.position())


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


def get_coords(repeat):
    for x in range(repeat):
        print(pg.position())
        time.sleep(1)


def display_menu(msp, cv, SPECIFY_NUM_TICKS):
    print("Type a Number and Press Enter:")
    print("1: Draw")
    print("2: Get Cursor Coords")
    print("3: Let's recalibrate")
    print("4: 4 corners")
    result = input()
    if result == "1":
        print("ctrl alt del to abort")
        ticks = 100
        if SPECIFY_NUM_TICKS:
            ticks = input()
        wait_loop(WAIT_SECONDS)
        cv.draw(msp, int(ticks))
        display_menu(msp, cv, SPECIFY_NUM_TICKS=False)

    if result == "2":
        print("For how long? (secs)")
        secs = input()
        get_coords(int(secs))
    if result == "3":
        cv = recaliberate(cv, CANVAS_VARIABLE=False)
    if result == "4":
        get_4_points(5)
    if result == "x":
        sys.exit()

    return cv


def main():

    cv = Canvas(900, 504, MANUAL_CANVAS=False)
    msp = MSPaint(5, MANUAL_COLOR=False, MANUAL_SIZE=False)
    # msp.pick_color("orange")
    # msp.click()
    # cv.draw_line((1200, 500), (1400, 500))
    msp.display_all_sizes()

    # cv = recaliberate(cv, CANVAS_VARIABLE=False)

    while True:
        cv = display_menu(msp, cv, SPECIFY_NUM_TICKS=False)


VERBOSE = True
SPECIFY_NUM_TICKS = False
NUM_COLOR_BUTTONS = (10, 2)
NUM_BRUSH_SIZES = 4
WAIT_SECONDS = 5
ONE_IN_10 = 90
ONE_IN_20 = 95

PALETTE = {
    "black": (1, 1),
    "darkred": (3, 1),
    "red": (4, 1),
    "orange": (5, 1),
    "yellow": (6, 1),
    "green": (7, 1),
    "blue": (9, 1),
    "purple": (10, 1),
    "white": (1, 2),
    "Gray25": (2, 2),
    "brown": (3, 2),
    "blue-gray": (9, 2),
    "lavender": (10, 2),
}


if __name__ == "__main__":
    main()

