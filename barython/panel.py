#!/usr/bin/env python3

import threading
import time


class Panel():
    _widgets_barrier = threading.Barrier(1)
    refresh = 0.1

    def draw(self):
        pass

    def update(self):
        if self._widget_barrier.n_waiting <= 1:
            self._widget_barrier.wait()
            self.draw()
            time.sleep(self.refresh)

    def run(self):
        thread_pool = []
        for widget in self.widgets:
            thread_pool.append(threading.Thread(
                target=widget.update, daemon=True
            ))