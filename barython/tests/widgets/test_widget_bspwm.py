
from collections import OrderedDict
import pytest

from barython.screen import Screen
from barython.widgets.bspwm import BspwmDesktopWidget, BspwmDesktopPoolWidget


@pytest.fixture
def basic_bspwm_desktop_widget():
    return BspwmDesktopWidget(
        fg_occupied="#FF000000", bg_occupied="#FFFFFF00",
        fg_free="#FF000001", bg_free="#FFFFFF01",
        fg_urgent="#FF000002", bg_urgent="#FFFFFF02",
        fg_monitor="#FF000003", bg_monitor="#FFFFFF03",
        fg_focused_occupied="#FF000004", bg_focused_occupied="#FFFFFF04",
        fg_focused_free="#FF000005", bg_focused_free="#FFFFFF05",
        fg_focused_urgent="#FF000006", bg_focused_urgent="#FFFFFF06",
        fg_focused_monitor="#FF000007", bg_focused_monitor="#FFFFFF07",
        padding=1, refresh=0
    )


@pytest.fixture
def basic_bspwm_desktop_pool_widget():
    return BspwmDesktopPoolWidget(
        fg_occupied="#FF000000", bg_occupied="#FFFFFF00",
        fg_free="#FF000001", bg_free="#FFFFFF01",
        fg_urgent="#FF000002", bg_urgent="#FFFFFF02",
        fg_focused_occupied="#FF000004", bg_focused_occupied="#FFFFFF04",
        fg_focused_free="#FF000005", bg_focused_free="#FFFFFF05",
        fg_focused_urgent="#FF000006", bg_focused_urgent="#FFFFFF06",
        padding=1, refresh=0
    )


def test_bspwm_desktop_widget_actions_desktop(basic_bspwm_desktop_widget):
    bspwm = basic_bspwm_desktop_widget
    expected = {1: "bspc desktop -f \"d\""}
    assert expected == bspwm._actions_desktop("d")


def test_bspwm_desktop_widget_actions_monitor(basic_bspwm_desktop_widget):
    bspwm = basic_bspwm_desktop_widget
    expected = {1: "bspc monitor -f \"m\""}
    assert expected == bspwm._actions_monitor("m")


def test_bspwm_desktop_widget_parse_desktop(basic_bspwm_desktop_widget):
    bspwm = basic_bspwm_desktop_widget
    template_result = (
        "%{{A1:bspc desktop -f \"q\":}}"
        "%{{B{}}}%{{F{}}} %{{F-}}%{{B-}}"
        "%{{B{}}}%{{F{}}}q%{{F-}}%{{B-}}"
        "%{{B{}}}%{{F{}}} %{{F-}}%{{B-}}"
        "%{{A}}"
    )

    assoc_colors_prefix = {
        "O": (bspwm.bg_focused_occupied, bspwm.fg_focused_occupied),
        "o": (bspwm.bg_occupied, bspwm.fg_occupied),
        "F": (bspwm.bg_focused_free, bspwm.fg_focused_free),
        "f": (bspwm.bg_free, bspwm.fg_free),
        "U": (bspwm.bg_focused_urgent, bspwm.fg_focused_urgent),
        "u": (bspwm.bg_urgent, bspwm.fg_urgent),
    }

    for p, (fg, bg) in assoc_colors_prefix.items():
        expected = template_result.format(*((fg, bg) * 3))
        assert expected == "".join(bspwm._parse_desktop(p + "q", "_"))


def test_bspwm_desktop_widget_sort_fixed_order(basic_bspwm_desktop_widget):
    bspwm = basic_bspwm_desktop_widget
    desktops = ["us", "fqsd", "Oq", "ff"]
    fixed_order = ("q", "s", "qsd", "ff")
    bspwm.fixed_order = fixed_order
    assert bspwm._sort_fixed_order(desktops) == ["Oq", "us", "fqsd", "ff"]


def test_bspwm_desktop_widget_organize_result(basic_bspwm_desktop_widget):
    bspwm = basic_bspwm_desktop_widget
    monitors = OrderedDict([
        ('HDMI-0',
            {'desktops': ['Of'], 'layout': 'T', 'focused': True}),
        ('DVI-D-0',
            {'desktops':
                ['fo', 'f7', 'fDesktop2', 'os', 'oq', 'fp', 'fi', 'Ou'],
             'layout': 'T', 'focused': False}),
        ('DVI-I-0', {'desktops': ['Od'], 'layout': 'T', 'focused': False})
    ])

    expected = (
        "%{A1:bspc monitor -f \"HDMI-0\":}"
        "%{B#FFFFFF07}%{F#FF000007} %{F-}%{B-}"
        "%{B#FFFFFF07}%{F#FF000007}HDMI-0%{F-}%{B-}"
        "%{B#FFFFFF07}%{F#FF000007} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"f\":}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004}f%{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc monitor -f \"DVI-D-0\":}"
        "%{B#FFFFFF03}%{F#FF000003} %{F-}%{B-}"
        "%{B#FFFFFF03}%{F#FF000003}DVI-D-0%{F-}%{B-}"
        "%{B#FFFFFF03}%{F#FF000003} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"o\":}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001}o%{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"7\":}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001}7%{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"Desktop2\":}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001}Desktop2%{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"s\":}"
        "%{B#FFFFFF00}%{F#FF000000} %{F-}%{B-}"
        "%{B#FFFFFF00}%{F#FF000000}s%{F-}%{B-}"
        "%{B#FFFFFF00}%{F#FF000000} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"q\":}"
        "%{B#FFFFFF00}%{F#FF000000} %{F-}%{B-}"
        "%{B#FFFFFF00}%{F#FF000000}q%{F-}%{B-}"
        "%{B#FFFFFF00}%{F#FF000000} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"p\":}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001}p%{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"i\":}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001}i%{F-}%{B-}"
        "%{B#FFFFFF01}%{F#FF000001} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"u\":}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004}u%{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc monitor -f \"DVI-I-0\":}"
        "%{B#FFFFFF03}%{F#FF000003} %{F-}%{B-}"
        "%{B#FFFFFF03}%{F#FF000003}DVI-I-0%{F-}%{B-}"
        "%{B#FFFFFF03}%{F#FF000003} %{F-}%{B-}"
        "%{A}"
        "%{A1:bspc desktop -f \"d\":}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004}d%{F-}%{B-}"
        "%{B#FFFFFF04}%{F#FF000004} %{F-}%{B-}"
        "%{A}"
    )

    assert expected == "".join(bspwm.organize_result(monitors))


def test_bspwm_desktop_pool_widget_actions_desktop_no_screen(
        basic_bspwm_desktop_pool_widget):
    bspwm = basic_bspwm_desktop_pool_widget
    expected = {1: "bspc monitor -f \"m\""}
    assert expected == bspwm._actions_monitor("m")


def test_bspwm_desktop_pool_widget_actions_desktop_different_screen(
        basic_bspwm_desktop_pool_widget):
    """
    Test action for a focused desktop on different screen
    """
    bspwm = basic_bspwm_desktop_pool_widget
    # simulate the focus on the desktop d of monitor HDMI-0
    bspwm._focused["HDMI-0"] = "d"

    s = Screen("HDMI-0")
    s.add_widget("l", bspwm)
    expected = {1: "bspc desktop \"q\" -s \"d\""}
    assert expected == bspwm._actions_desktop("q", "HDMI-1")


def test_bspwm_desktop_pool_widget_actions_desktop_same_screen(
        basic_bspwm_desktop_pool_widget):
    bspwm = basic_bspwm_desktop_pool_widget
    # simulate the focus on the desktop d of monitor HDMI-0
    bspwm._focused["HDMI-0"] = "d"

    expected = {1: "bspc desktop -f \"q\""}
    assert expected == bspwm._actions_desktop("q", "HDMI-0")
