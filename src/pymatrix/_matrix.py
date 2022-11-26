import curses
from collections import deque

from _log import logger


class Config:
    chars = [
        (0x00000021, 1 + 0x0000007E),  # Basic Latin
        (0x000000BF, 1 + 0x000000FF),  # Latin-1 Supplement
        (0x00000100, 1 + 0x0000017F),  # Latin Extended-A
        (0x00000180, 1 + 0x0000024F),  # Latin Extended-B
        (0x00000250, 1 + 0x000002AF),  # IPA
        (0x000002B0, 1 + 0x000002FF),  # Spacing Modifier Letters
    ]
    whites = [255]
    greens = [47, 35]
    show = [-16, -8, 32, 128]
    # show when value <= 0, green when value < 0, white when value = 0
    speed = 512  # BPM


class Cell:
    def __init__(self, char: str, hide: bool, color: int):
        self._char = char[0]
        self._hide = hide
        self._color = color


class Line(deque):
    def __init__(self, n: int):
        self._cells = deque()
        for i in range(n):
            self.shift()

    def shift(self):
        ...


class Matrix:
    def render(self, window: curses.window):
        logger.debug(window)
