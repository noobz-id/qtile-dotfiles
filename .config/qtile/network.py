# lib
import time
import psutil

from libqtile.widget import base


class DynamicNet(base.InLoopPollText):

    defaults = [
       ("update_interval", 1.0, "The update interval in seconds")
    ]

    def __init__(self, **config):
        # register to qtile widget
        base.InLoopPollText.__init__(self, "", **config)
        self.add_defaults(DynamicNet.defaults)
        # internal state
        self._last_recv = 0
        self._last_sent = 0
        self._last_time = time.time()

    def _bytes_format(self, size):
        # converter
        for unit in ['B', 'K', 'M', 'G']:
            if size < 1024:
                # ok
                return f"{int(size)}{unit}" if unit == 'B' else f"{size:.1f}{unit}"
            #
            size /= 1024
        # fallback
        return f"{size:.1f}T"

    def _active_interface(self):
        # read interface route
        with open("/proc/net/route", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) < 2 or parts[1] == 'Destination':
                    continue
                # check is primary route
                if parts[1] == '00000000':
                    # interface name
                    return parts[0]
        # not exist
        return None

    def poll(self):
        # this is main loop called by qtile
        try:
            # get interface
            interface = self._active_interface()
            # get interface list
            stats = psutil.net_io_counters(pernic=True).get(interface)
            # check timer
            now = time.time()
            elapsed = now - self._last_time
            if elapsed <= 0:
                # return prev text when polling too fast
                return self.text
            # calculate speed
            down_speed = (stats.bytes_recv - self._last_recv) / elapsed
            up_speed = (stats.bytes_sent - self._last_sent) / elapsed
            # update state for next poll
            self._last_recv = stats.bytes_recv
            self._last_sent = stats.bytes_sent
            self._last_time = now
            # format speed
            down_fmt = self._bytes_format(down_speed)
            up_fmt = self._bytes_format(up_speed)
            # ok
            return f"{interface}: {up_fmt}/{down_fmt}"
        except Exception:
            # reset counter (prevent spike at back-online)
            self._last_recv = 0
            self._last_sent = 0
            #
            return "offline"

