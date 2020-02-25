import pyautogui as pg

from utils import *
from draw import *

NUM_COLOR_BUTTONS = (10, 2)
NUM_BRUSH_SIZES = 4


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

    def pick_item(
        self, item_type="color", selected="", palette={}, brushes={}, sizes={}
    ):

        if item_type == "color":
            if selected == "":
                color = random.choice(list(palette.keys()))
            else:
                color = selected
                palette = get_color_index_dict([color])
                if VERBOSE:
                    print(color)
            print(f" switching to {color}")
            color_xy = self.get_selected_items_coords(item_type, color, palette=palette)
            # print(f"{color} @ {color_xy}")
            pg.moveTo(color_xy)
            time.sleep(0.5)
            pg.click(color_xy)  # select the color

        if item_type == "brush_size":
            pg.moveTo(self.brush_size_btn)
            pg.click()

            if selected == "":
                selected = random.choice(list(sizes.keys()))

            b_index = sizes[selected]
            print(f" switching to Brush size{b_index} {selected}")
            brush_size_y = self.size_options[b_index]  # convert index to y coord

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
                style = random.choice(list(brushes.keys()))
            else:
                style = selected

            pos_xy = self.get_selected_items_coords(item_type, style)
            print(f"{item_type} {style} @ {pos_xy}")

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

        active_brushes = get_active_brushes(art_direction)

        if action_type == "click":
            if item_type == "brush_style":
                for k, _ in active_brushes.items():
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
                for k, _ in active_brushes.items():
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
                for i, k in enumerate(active_brushes):
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

