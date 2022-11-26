import curses
import os
import random
import time

from _log import logger


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


def _get_color(i: int):
    return i, random.choice(PARAMETERS['greens' if i < 0 else 'whites'])


def _refresh(i: int, c):
    res: int = 0
    '''
    = 0 -> negative
    =-1 -> positive
    > 0 -> -1
    <-1 -> +1
    '''
    if i == 0:
        res = random.randint(*PARAMETERS['show'][:2])
    elif i == -1:
        res = random.randint(*PARAMETERS['show'][2:])
    elif i > 0:
        res = i - 1
    elif i < -1:
        res = i + 1
    return _get_color(res)


def get_nstr(columns: int, lines: int):
    show = [
        [
            _get_color(random.randint(PARAMETERS['show'][0], PARAMETERS['show'][-1]))
            for c in range(columns)
        ]
    ]
    while len(show) < lines:
        show = [[_refresh(*s) for s in show[0]]] + show
    char = [
        [random.choice(PARAMETERS['chars']) for c in range(columns)]
        for l in range(lines)
    ]
    while True:
        for l in range(len(show)):
            for c in range(len(show[l])):
                if show[l][c] == -1:
                    char[l][c] = random.choice(PARAMETERS['chars'])
        show = [[_refresh(*s) for s in show[0]]] + show[:-1]
        yield show, char


def render(window: curses.window, show, char):
    for l in range(len(show)):
        for c in range(len(show[l]) - 1):
            try:
                window.addstr(
                    l,
                    c,
                    char[l][c] if show[l][c][0] <= 0 else ' ',
                    curses.color_pair(show[l][c][1]),
                )
            except:
                ...
                logger.debug('change terminal size')


def main(window: curses.window):
    terminal_size = os.get_terminal_size()
    nstr = get_nstr(*terminal_size)
    window.timeout(0)
    while terminal_size == os.get_terminal_size():
        try:
            # k = window.getkey()
            ...
        except Exception as exception:
            logger.exception(exception)
        else:
            ...
            # if k != 'KEY_RESIZE':
            #     return k
        show, char = next(nstr)
        render(window, show, char)
        window.refresh()
        time.sleep(60 / PARAMETERS['speed'])
