#!/usr/bin/env python3

import logging
import xpybutil

from . import _Hook
from barython.tools import splitted_sleep

logger = logging.getLogger("xorg_hook")


class _XorgHook(_Hook):
    """
    Base for hooks related to xorg
    """
    def parse_event(self, events=None):
        """
        Parse event and return a kwargs meant be used by notify() then
        """
        return {"events": list(events), }

    def subscribe_to(self, xpybutil):
        """
        Subscribe to events

        :param xpybutil: local import of xpybutil
        """
        return NotImplementedError()

    def run(self):
        # Import locally to not globalize the subscriptions to the entire file
        import xpybutil
        self.subscribe_to(xpybutil)
        while not self._stop_event.is_set():
            try:
                xpybutil.event.read()
                if len(xpybutil.event.peek()):
                    logger.debug("Xorg events received")
                    self.notify(
                        **self.parse_event(events=xpybutil.event.queue())
                    )
            except Exception as e:
                logger.error(e)
            finally:
                splitted_sleep(self.refresh, stop=self._stop_event.is_set)

    def is_compatible(self, hook):
        return True

    def __init__(self, refresh=0.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if refresh == -1:
            refresh = 0.5
        self.refresh = refresh


class WindowHook(_XorgHook):
    """
    Listen on Xorg events related to windows
    """
    def parse_event(self, events=None):
        return {
            "events": [(e, xpybutil.util.get_atom_name(e.atom))
                       for e in events]
        }

    def subscribe_to(self, xpybutil):
        import xpybutil.window
        xpybutil.window.listen(xpybutil.root, "PropertyChange")
