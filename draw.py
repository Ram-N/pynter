import pyautogui as pg


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
