# This file is part of nvitop, the interactive NVIDIA-GPU process viewer.
# This file is originally part of ranger, the console file manager. https://github.com/ranger/ranger
# License: GNU GPL version 3.

# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from __future__ import annotations

import curses
from typing import TYPE_CHECKING, ClassVar


if TYPE_CHECKING:
    from typing_extensions import Self  # Python 3.11+


__all__ = ['MouseEvent']


class MouseEvent:
    PRESSED: ClassVar[tuple[int, ...]] = (
        0,
        curses.BUTTON1_PRESSED,
        curses.BUTTON2_PRESSED,
        curses.BUTTON3_PRESSED,
        curses.BUTTON4_PRESSED,
    )
    RELEASED: ClassVar[tuple[int, ...]] = (
        0,
        curses.BUTTON1_RELEASED,
        curses.BUTTON2_RELEASED,
        curses.BUTTON3_RELEASED,
        curses.BUTTON4_RELEASED,
    )
    CLICKED: ClassVar[tuple[int, ...]] = (
        0,
        curses.BUTTON1_CLICKED,
        curses.BUTTON2_CLICKED,
        curses.BUTTON3_CLICKED,
        curses.BUTTON4_CLICKED,
    )
    DOUBLE_CLICKED: ClassVar[tuple[int, ...]] = (
        0,
        curses.BUTTON1_DOUBLE_CLICKED,
        curses.BUTTON2_DOUBLE_CLICKED,
        curses.BUTTON3_DOUBLE_CLICKED,
        curses.BUTTON4_DOUBLE_CLICKED,
    )
    CTRL_SCROLLWHEEL_MULTIPLIER: ClassVar[int] = 5

    def __init__(self, state: tuple[int, int, int, int, int]) -> None:
        """Create a MouseEvent object from the result of win.getmouse()."""
        _, self.x, self.y, _, self.bstate = state

        # x-values above ~220 suddenly became negative, apparently
        # it's sufficient to add 0xFF to fix that error.
        if self.x < 0:
            self.x += 0xFF
        if self.y < 0:
            self.y += 0xFF

    @classmethod
    def get(cls) -> Self:
        """Get the mouse event."""
        return cls(curses.getmouse())

    def pressed(self, n: int) -> bool:
        """Return whether the mouse key n is pressed."""
        try:
            return bool(self.bstate & self.PRESSED[n])
        except IndexError:
            return False

    def released(self, n: int) -> bool:
        """Return whether the mouse key n is released."""
        try:
            return bool(self.bstate & self.RELEASED[n])
        except IndexError:
            return False

    def clicked(self, n: int) -> bool:
        """Return whether the mouse key n is clicked."""
        try:
            return bool(self.bstate & self.CLICKED[n])
        except IndexError:
            return False

    def double_clicked(self, n: int) -> bool:
        """Return whether the mouse key n is double clicked."""
        try:
            return bool(self.bstate & self.DOUBLE_CLICKED[n])
        except IndexError:
            return False

    def wheel_direction(self) -> int:
        """Return the direction of the scroll action, 0 if there was none."""
        # If the bstate > ALL_MOUSE_EVENTS, it's an invalid mouse button.
        # I interpret invalid buttons as "scroll down" because all tested
        # systems have a broken curses implementation and this is a workaround.
        # Recently it seems to have been fixed, as 2**21 was introduced as
        # the code for the "scroll down" button.
        if self.pressed(4):
            return -self.CTRL_SCROLLWHEEL_MULTIPLIER if self.ctrl() else -1
        if self.pressed(2) or (self.bstate & (1 << 21)) or self.key_invalid():
            return self.CTRL_SCROLLWHEEL_MULTIPLIER if self.ctrl() else 1
        return 0

    def ctrl(self) -> bool:
        return bool(self.bstate & curses.BUTTON_CTRL)

    def alt(self) -> bool:
        return bool(self.bstate & curses.BUTTON_ALT)

    def shift(self) -> bool:
        return bool(self.bstate & curses.BUTTON_SHIFT)

    def key_invalid(self) -> bool:
        return self.bstate > curses.ALL_MOUSE_EVENTS
