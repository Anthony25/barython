#!/usr/bin/env python3


class Panel():
    refresh = 0.1
    _screens = None

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

    def __init__(self, refresh=None, screens=None):
        self.refresh = self.refresh if refresh is None else refresh
        self._screens = self._screens if screens is None else screens
        if not self._screens:
            self._screens = []
