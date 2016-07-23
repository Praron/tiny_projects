from copy import deepcopy
import curses
from random import randint
from logging import debug
import logging
import os

os.remove('debug.log')
logging.basicConfig(format='%(message)s', level=logging.DEBUG,
                    filename='debug.log')

WHITE = curses.COLOR_WHITE
BLACK = curses.COLOR_BLACK
RED = curses.COLOR_RED
BLUE = curses.COLOR_BLUE
CYAN = curses.COLOR_CYAN
GREEN = curses.COLOR_GREEN
YELLOW = curses.COLOR_YELLOW
MAGNETA = curses.COLOR_MAGENTA

BACKGROUND_PAIR = 0
LIVE_CELL_PAIR = 1
DEAD_CELL_PAIR = 2
CURSOR_PAIR = 3

W = 30
H = 10
# W = 150
# H = 12

WRAP = False
BORDERLESS_GEN = True


def init_pairs():
    global LIVE_CELL_PAIR, DEAD_CELL_PAIR
    global CURSOR_PAIR
    curses.init_pair(DEAD_CELL_PAIR, BLACK, CYAN)
    curses.init_pair(LIVE_CELL_PAIR, WHITE, RED)
    curses.init_pair(CURSOR_PAIR, WHITE, GREEN)
    DEAD_CELL_PAIR = curses.color_pair(DEAD_CELL_PAIR)
    LIVE_CELL_PAIR = curses.color_pair(LIVE_CELL_PAIR)
    CURSOR_PAIR = curses.color_pair(CURSOR_PAIR)


def init_scr(scr):
    scr.clear()
    curses.curs_set(False)
    init_pairs()
    # curses.halfdelay(5)


def get_key(scr):
    try:
        return scr.getkey()
    except curses.error:
        return 'no_input'


def to_str(*args):
    return(' '.join(map(str, args)))


def list_2d_to_str(arr):
    string = ''
    for row in arr:
        for el in row:
            string += str(el)
        string += '\n'
    return string


def get_2d_slice(arr, p1, p2):
    return [arr[row][p1[1]:p2[1]] for row in range(p1[0], p2[0])]
    # return [arr[row][p1[1]:p2[1] + 1] for row in range(p1[0], p2[0] + 1)]


# def insert_2d_list(origin, source, start):
#     new_list = deepcopy(origin)
#     h, w = len(source[0]), len(source)
#     for y in range(h):
#         for x in range(w):
#             new_list[start[0] + x][start[1] + y] = source[x][y]
#     return new_list


def next_gen(arr, p1=(0, 0), p2=(W, H)):
    w, h = p2[0] - p1[0], p2[1] - p1[1]
    # w, h = len(arr), len(arr[0])
    new_arr = deepcopy(arr)
    if p1 != (0, 0):
        debug(to_str('w, h: ', w, h))
        debug(to_str('points: ', p1, p2))
        debug(list_2d_to_str(get_2d_slice(arr, p1, p2)))
    # new_arr = [[0] * H for _ in range(W)]
    # new_arr = [[0] * h for _ in range(w)]
    for y in range(p1[1], p2[1]):
        for x in range(p1[0], p2[0]):
            neighbors = [(x + dx, y + dy)
                         for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                         if not dx == dy == 0]
            # live_neighbors = len(list(filter(lambda n:
            #                                  arr[n[0] % w][n[1] % h] == 1,
            #                                  neighbors)))
            if not WRAP:
                def f(n):
                    try:
                        if n[0] < 0 or n[1] < 0 or n[0] > W + 1 or n[1] > H + 1:
                            return 0
                        return arr[n[0]][n[1]] == 1
                    except IndexError:
                        return False
                # f = (lambda n: arr[clamp(0, n[0], w)][clamp(0, n[1], h)] == 1)
                     # if n[0] in range(w) and n[1] in range(h) else False)
                live_neighbors = len(list(filter(f, neighbors)))

            if live_neighbors == 3 or (arr[x][y] == 1 and live_neighbors == 2):
                new_arr[x][y] = 1
            else:
                new_arr[x][y] = 0
            if p1 != (0, 0):
                debug(to_str(live_neighbors))
    if p1 != (0, 0):
        debug('---')
        debug(list_2d_to_str(get_2d_slice(new_arr, p1, p2)))
    return new_arr


def draw_state(scr, state):
    for y in range(H):
        for x in range(W):
            ch = ' '
            pair = LIVE_CELL_PAIR if state[x][y] == 1 else DEAD_CELL_PAIR
            scr.addch(y, x, ch, pair)


def draw_hint(scr, state):
    hint = next_gen(state)
    for y in range(H):
        for x in range(W):
            ch = '#' if hint[x][y] == 1 else ' '
            pair = LIVE_CELL_PAIR if state[x][y] == 1 else DEAD_CELL_PAIR
            scr.addch(y, x, ch, pair)


def clamp(min, x, max):
    return sorted((min, x, max))[1]


def flip(x):
    return abs(x - 1)


def input_point(scr, state, sel_point=None):
    x, y = 0, 0
    if sel_point is not None:
        x, y = sel_point[0], sel_point[1]
    key = None
    while key != ' ':
        draw_state(scr, state)
        draw_hint(scr, state)
        scr.addch(y, x, '@', CURSOR_PAIR)

        if sel_point is not None:
            # x_fix = 1 if sel_point[0] - x < 0 else 0
            # y_fix = 1 if sel_point[1] - y < 0 else 0
            # x_fix = 0
            # y_fix = 0
            hint = next_gen(state)
            # for sel_y in range(*sorted([sel_point[1] + flip(y_fix),
            #                             min([y + y_fix, H])])):
            #     for sel_x in range(*sorted([sel_point[0] + flip(x_fix),
            #                                 min([x + x_fix, W])])):
            hor = sorted([sel_point[0], min([x, W])])
            hor[1] = hor[1] + 1
            ver = sorted([sel_point[1], min([y, H])])
            ver[1] = ver[1] + 1
            for sel_y in range(*ver):
                for sel_x in range(*hor):
            # for sel_y in range(*sorted([sel_point[1],
            #                             min([y, H])])):
                # for sel_x in range(*sorted([sel_point[0],
                #                             min([x, W])])):
                    scr.addch(sel_y, sel_x, '#' if hint[sel_x][sel_y] == 1
                              else '%' if state[sel_x][sel_y] == 1 else ' ',
                              CURSOR_PAIR)

        key = get_key(scr)
        if key in 'hl':
            x += 1 if key == 'l' else -1
        if key in 'jk':
            y += 1 if key == 'j' else -1
        x = clamp(0, x, W - 1)
        y = clamp(0, y, H - 1)
    return (x, y)


def input_selection(scr, state):
    p1 = input_point(scr, state)
    p2 = input_point(scr, state, p1)
    p2 = (min(p2[0] + 1, W), min(p2[1] + 1, H))
    return sorted((p1, p2), key=lambda p: p[0])


def main(stdscr):
    init_scr(stdscr)
    state = [[randint(0, 1) for row in range(H)] for col in range(W)]

    while True:
        draw_state(stdscr, state)
        draw_hint(stdscr, state)

        key = get_key(stdscr)
        if key == 'q':
            break
        if key == 'r':
            state = [[randint(0, 1) for row in range(H)] for col in range(W)]
        if key == 'a':
            p1, p2 = input_selection(stdscr, state)
            state = next_gen(state, p1, p2)
            # state = next_state(state, p1, p2)

        if key == 'z':
            # state = next_state(state)
            state = next_gen(state)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
