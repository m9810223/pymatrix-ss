import curses
import sys

import _matrix
import _matrix_legacy
from _log import logger


class _Window:
    _window: curses.window

    def init(self) -> curses.window:
        self._window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._window.keypad(True)
        try:
            curses.start_color()
        except:
            pass
        return self._window

    def deinit(self):
        self._window.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        # logger.debug('deinit')

    def __enter__(self):
        # logger.debug('__enter__')
        return self.init()

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()
        # logger.debug('__exit__')


class Window(_Window):
    def init(self):
        super().init()
        # cursor state:0 for invisible, 1 for normal visible, or 2 for very visible.
        curses.curs_set(0)
        return self._window

    def _set_color(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        for i in range(256):
            self._window.addstr(str(i), curses.color_pair(i))
            self._window.addstr(' ', curses.color_pair(i))
        self._window.getch()

    def print_color_code(self):
        with self:
            self._set_color()

    def screensaver_legacy(self):
        with self as window:
            _matrix_legacy.main(window)

    def screensaver(self):
        with self as window:
            _matrix.Matrix().render(window)


if __name__ == '__main__':
    window = Window()
    try:
        # window.screensaver_legacy()
        window.screensaver()
    except KeyboardInterrupt:
        sys.exit(0)
