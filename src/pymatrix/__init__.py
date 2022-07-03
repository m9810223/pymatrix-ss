#!/usr/bin/env python3

import curses
from os import get_terminal_size
from random import choice
from random import randint
from time import sleep


PARAMETERS = {
    'chars': ''.join(
        (
            chr(x)
            for r in (
                range(*_)
                for _ in (
                    # (33, 34),
                    (0x00000021, 1 + 0x0000007E),  # Basic Latin
                    (0x000000BF, 1 + 0x000000FF),  # Latin-1 Supplement
                    (0x00000100, 1 + 0x0000017F),  # Latin Extended-A
                    (0x00000180, 1 + 0x0000024F),  # Latin Extended-B
                    (0x00000250, 1 + 0x000002AF),  # IPA
                    (0x000002B0, 1 + 0x000002FF),  # Spacing Modifier Letters
                )
            )
            for x in r
        )
    ),
    'whites': [255],
    'greens': [47, 35],
    # show when value <= 0, green when value < 0, white when value = 0
    'show': [-16, -8, 32, 128],
    'speed': 512,  # BPM
}


def init():
    window = curses.initscr()
    curses.noecho()
    curses.cbreak(True)
    window.keypad(True)
    try:
        curses.start_color()
    except:
        pass
    curses.use_default_colors()

    for i in range(curses.COLORS):
        curses.init_pair(i, i - 1, -1)

    return window


def deinit(window: curses.window):
    window.keypad(False)
    curses.echo(True)
    curses.nocbreak()
    curses.endwin()


def _get_color(i):
    return i, choice(PARAMETERS['greens' if i < 0 else 'whites'])


def _refresh(i, c):
    '''
    = 0 -> negative
    =-1 -> positive
    > 0 -> -1
    <-1 -> +1
    '''
    if i == 0:
        res = randint(*PARAMETERS['show'][:2])
    elif i == -1:
        res = randint(*PARAMETERS['show'][2:])
    elif i > 0:
        res = i - 1
    elif i < -1:
        res = i + 1
    return _get_color(res)


def get_nstr(columns, lines):
    show = [
        [
            _get_color(randint(PARAMETERS['show'][0], PARAMETERS['show'][-1]))
            for c in range(columns)
        ]
    ]
    while len(show) < lines:
        show = [[_refresh(*s) for s in show[0]]] + show
    char = [[choice(PARAMETERS['chars']) for c in range(columns)] for l in range(lines)]
    while True:
        for l in range(len(show)):
            for c in range(len(show[l])):
                if show[l][c] == -1:
                    char[l][c] = choice(PARAMETERS['chars'])
        show = [[_refresh(*s) for s in show[0]]] + show[:-1]
        yield show, char


def render(window: curses.window, show, char):
    for l in range(len(show)):
        for c in range(len(show[l]) - 1):
            window.addstr(
                l,
                c,
                char[l][c] if show[l][c][0] <= 0 else ' ',
                curses.color_pair(show[l][c][1]),
            )


def main(window: curses.window):
    terminal_size = get_terminal_size()
    nstr = get_nstr(*terminal_size)
    window.timeout(0)
    while terminal_size == get_terminal_size():
        try:
            k = window.getkey()
        except:
            pass
        else:
            if k != 'KEY_RESIZE':
                return k
        show, char = next(nstr)
        render(window, show, char)
        window.refresh()
        sleep(60 / PARAMETERS['speed'])


def print_color_code():
    def p(stdscr: curses.window):
        curses.start_color()
        curses.use_default_colors()
        for i in range(curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        for i in range(256):
            stdscr.addstr(str(i), curses.color_pair(i))
            stdscr.addstr(' ', curses.color_pair(i))
        stdscr.getch()

    curses.wrapper(p)
    exit()


def screensaver():
    # print_color_code()
    try:
        while True:
            window = init()
            key = main(window)
            if key:
                exit()
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
    finally:
        deinit(window)


if __name__ == '__main__':
    screensaver()
