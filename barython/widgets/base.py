#!/usr/bin/env python3

import logging
import shlex
import subprocess
import threading
import time


logger = logging.getLogger("barython")


class Widget():
    """
    Basic Widget
    """
    #: cache the content after update
    _content = None
    #: refresh rate
    _refresh = 0
    #: screens linked. Used for callbacks
    screens = None
    #: background for the widget
    bg = None
    #: foreground for the widget
    fg = None
    #: padding
    padding = 0
    #: list of fonts index used
    fonts = None
    #: dictionnary of actions
    actions = None

    @property
    def content(self):
        return self._content

    @property
    def refresh(self):
        if self._refresh == 0 and self.screens is not None:
            return min([screen.refresh for screen in self.screens])
        else:
            return self._refresh

    @refresh.setter
    def refresh(self, value):
        self._refresh = value

    def decorate(self, text, fg=None, bg=None, padding=0, font=None,
                 actions=None):
        """
        Decorate a text with custom properties

        :param fg: foreground
        :param bg: background
        :param padding: padding around the text
        :param font: index of font to use
        :param actions: dict of actions
        """
        try:
            joined_actions = "".join(
                "%{{A{}:{}:}}".format(a, cmd) for a, cmd in actions.items()
            )
        except (TypeError, AttributeError):
            joined_actions = ""
        return (9*"{}").format(
            joined_actions,
            "%{{B{}}}".format(bg) if fg else "",
            "%{{F{}}}".format(fg) if fg else "",
            "%{{T{}}}".format(font) if font else "",
            text.center(len(text) + 2*padding),
            "%{{T-}}".format(font) if font else "",
            "%{F-}" if fg else "",
            "%{B-}" if bg else "",
            "%{A}" * len(actions) if actions else "",
        )

    def decorate_with_self_attributes(self, text, *args, **kwargs):
        """
        Return self.decorate but uses self attributes for default values
        """
        d_kwargs = {
            "fg": self.fg, "bg": self.bg, "padding": self.padding,
            "font": self.fonts[0] if self.fonts else None,
            "actions": self.actions, **kwargs
        }
        for parameter, value in zip(("fg", "bg", "padding", "font", "actions"),
                                    args):
            d_kwargs[parameter] = value

        return self.decorate(text, **d_kwargs)

    def _update_screens(self, new_content):
        """
        If content has changed, request the screen update
        """
        if self._content != new_content:
            self._content = new_content
            for screen in self.screens:
                screen.update()

    def update(self):
        pass

    def __init__(self, bg=None, fg=None, padding=None, fonts=None,
                 actions=None, refresh=None, screens=None):
        self.bg = self.bg if bg is None else bg
        self.fg = self.fg if fg is None else fg
        self.fonts = self.fonts if fonts is None else fonts
        if self.fonts is None:
            self.fonts = tuple()
        self.actions = self.actions if actions is None else actions
        if self.actions is None:
            self.actions = dict()
        self.padding = self.padding if padding is None else padding
        if refresh is not None:
            self._refresh = refresh
        self.screens = self.screens if screens is None else self.screens
        if not self.screens:
            self.screens = set()


class TextWidget(Widget):
    text = ""

    def update(self):
        new_content = self.decorate_with_self_attributes(self.text)
        self._update_screens(new_content)

    def start(self):
        self.update()

    def __init__(self, text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = self.text if text is None else text


class ThreadedWidget(Widget):
    lock_start = None

    def update(self, new_content=None, *args, **kwargs):
        threading.Thread(
            target=self._update_screens, args=(new_content,)
        ).start()

    def start(self):
        with self.lock_start:
            t = threading.Thread(target=self.update)
            t.start()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock_start = threading.Lock()


class SubprocessWidget(ThreadedWidget):
    """
    Run a subprocess in a loop
    """
    #: command to run. Can be an iterable or a string
    cmd = None
    #: value for the subprocess.Popen shell parameter. Default to False
    shell = False

    def update(self, *args, **kwargs):
        def init_subprocess(cmd):
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            return subprocess.Popen(
                cmd, stdout=subprocess.PIPE, shell=self.shell
            )

        subproc = init_subprocess(self.cmd)
        while True:
            try:
                output = subproc.stdout.readline()
                finished = subproc.poll()
                if output != b"":
                    new_content = self.decorate_with_self_attributes(
                        output.decode().replace('\n', '').replace('\r', '')
                    )
                    super().update(new_content=new_content, *args, **kwargs)
                if finished is not None:
                    subproc = init_subprocess(self.cmd)
            except Exception as e:
                logger.error(e)
                subproc = init_subprocess(self.cmd)
            finally:
                time.sleep(self.refresh)

    def __init__(self, cmd=None, shell=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = self.cmd if cmd is None else cmd
        self.shell = self.shell if shell is None else shell
