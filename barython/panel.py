#!/usr/bin/env python3


import signal
import threading


class Panel():
    #: launch one bar per screen or use only one with %{S+}
    instance_per_screen = True
    #: command for lemonbar
    bar_cmd = "lemonbar"
    #: refresh rate
    refresh = 0.1
    #: screens attached to this panel
    _screens = None
    _stop = None

    def add_screen(self, *screens, index=None):
        """
        Add a screen to the panel

        :param alignment: where adding the screen (left, center, right)
        :param *screens: screens to add
        :param index: if set, will insert the screens before the specified
                      index (default: None)
        """
        if index is None:
            self._screens.extend(screens)
        else:
            new_screen_list = (
                self._screens[:index] + list(screens) + self._screens[index:]
            )
            self._screens = new_screen_list
        for s in self._screens:
            s.panel = self

    def start(self):
        self._stop.clear()
        try:
            signal.signal(signal.SIGINT, self.stop)
        except ValueError:
            pass
        for screen in self._screens:
            threading.Thread(
                target=screen.start
            ).start()
        self._stop.wait()
        for screen in self._screens:
            screen.stop()

    def stop(self, *args, **kwargs):
        """
        Stop the screen
        """
        self._stop.set()

    def __init__(self, refresh=None, screens=None):
        self.refresh = self.refresh if refresh is None else refresh
        self._screens = self._screens if screens is None else screens
        if not self._screens:
            self._screens = []
        self._stop = threading.Event()
