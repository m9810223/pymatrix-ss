import curses
import random
import string
from collections import deque

from _log import logger


class Cell:
    def __init__(self, char: str, hide: bool, color: int):
        self._char = char[0]
        self._hide = hide
        self._color = color

    def __repr__(self):
        return (
            f'<'
            f'{self.__class__.__name__}'
            f' char={self._char}'
            f' hide={self._hide}'
            f' color={self._color}'
            f'>'
        )


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
    # greens = [47, 35]
    greens = [47]
    show = [-16, -8, 32, 128]
    # show when value <= 0, green when value < 0, white when value = 0
    speed = 512  # BPM


class Line(deque):
    '''
    -: blank
    0: raindrop
    +: afterimage
    '''

    range_blank = [2, 2]
    range_rain = [1, 1]
    chars = string.ascii_uppercase

    @classmethod
    def random_index(cls):
        index = -random.randint(*cls.range_blank)
        assert index < 0
        return index

    @classmethod
    def random_stop(cls):
        stop = random.randint(*cls.range_rain)
        assert stop > 0
        return stop

    @classmethod
    def random_char(cls):
        return random.choice(cls.chars)

    def move_to(self, height: int):
        if self._height > height:
            self._height = height
            self._truncate()
            return
        if self._height < height:
            d = height - self._height
            self._height = height
            for _ in range(d):
                self.falling()
            return

    def __init__(self, height: int):
        self._height = 0
        self._speed = Config.speed
        self._cells: deque[Cell] = deque()
        self._index, self._stop = self.random_index(), self.random_stop()
        self.move_to(height)

    def falling(self):
        cell = self.create_cell()
        logger.debug(cell)
        self._cells.appendleft(cell)
        self._index += 1
        if self._index > self._stop:
            self._index = self.random_index()
        logger.debug(f'{self._index= }')
        self._truncate()

    def create_cell(self):
        return Cell(
            char=self.random_char(),
            hide=self._index >= 0,
            color=random.choice(Config.greens)
            if self._index
            else random.choice(Config.whites),
        )

    def _truncate(self):
        c = len(self._cells) - self._height
        for _ in range(c):
            self._cells.pop()

    def __repr__(self):
        logger.debug(self._cells)
        return (
            f'<'
            f'{self.__class__.__name__}'
            f' index={self._index}'
            f' speed={self._speed}'
            f'>'
        )


class Matrix:
    def adjust_to(self, amount: int):
        if self._amount > amount:
            self._amount = amount
            self._truncate()
            return
        if self._amount < amount:
            ...
            return

    def __init__(self, amount: int):
        self._amount = 0
        self._lines = []
        self.adjust_to(amount)

    def _truncate(self):
        c = len(self._lines) > self._amount
        for _ in range(c):
            self._lines.pop()

    def __repr__(self):
        return f'<' f'{self.__class__.__name__} ' f'>'


if __name__ == '__main__':
    m = Matrix(3)
