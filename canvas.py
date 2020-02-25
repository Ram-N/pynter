import pyautogui as pg

from utils import *
from draw import *


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

            if k == "BRUSHES":
                if len(vlist) == 1:
                    brush_change = False

            if k == "BRUSH-SIZES":
                if len(vlist) == 1:
                    size_change = False

        if "continuous" in art_direction["START_POINTS"]:
            continuous_flag = True
            endX, endY = get_start_pt(self, art_direction, specific="random")

        active_brushes = get_active_brushes(art_direction)
        active_sizes = get_active_sizes(art_direction)
        thresholds = get_thresholds(art_direction)

        print(f"Active Sizes {active_sizes}")
        print(f"thresholds {thresholds}")
        print(
            f"color_change={color_change} size change {size_change}, brush change {brush_change}"
        )

        # initialize Color, Size and Brush
        msp.pick_item(item_type="color", selected="", palette=palette)
        msp.pick_item(item_type="brush_size", selected="", sizes=active_sizes)
        msp.pick_item(item_type="brush_style", selected="", brushes=active_brushes)

        for stroke in range(num_strokes):

            if color_change and ("color_change" in thresholds):
                if random.randint(0, 100) > thresholds["color_change"]:
                    msp.pick_item(item_type="color", selected="", palette=palette)

            if size_change and ("size_change" in thresholds):
                if random.randint(0, 100) > thresholds["size_change"]:
                    msp.pick_item(
                        item_type="brush_size", selected="", sizes=active_sizes
                    )

            if brush_change and ("brush_change" in thresholds):
                if random.randint(0, 100) > thresholds["brush_change"]:
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
