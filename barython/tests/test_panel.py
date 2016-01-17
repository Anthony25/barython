
import pytest

from barython.panel import Panel
from barython.screen import Screen


def test_panel_no_widget():
    Panel()


def test_pannel_add_screen():
    p = Panel()
    assert len(p._screens) == 0

    s = Screen()
    p.add_screen(s)
    assert p._screens[0] == s


def test_pannel_add_screen_insert():
    p = Panel()
    s = Screen()
    s1 = Screen()
    s2 = Screen()

    p.add_screen(s, s2)
    p.add_screen(s1, index=1)

    assert len(p._screens) == 3
    for screen, pscreen in zip((s, s1, s2), p._screens):
        assert screen == pscreen