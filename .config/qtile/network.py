# lib
import socket
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
        # setup socket 
        self._socket = None
        self._create_socket()

    def _create_socket(self):
        # close first
        try: self._socket.close()
        except: pass
        # create new
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(0.2)

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
        try:
            # connect(less) udp
            self._socket.connect(("8.8.8.8", 53))
            # get local ip
            local_ip = self._socket.getsockname()[0]
            # find interface name
            for name, addrs in psutil.net_if_addrs().items():
                # matching address
                if any(addr.address == local_ip for addr in addrs):
                    # ok
                    return name
            # interface not found
            return None
        except (socket.error, OSError):
            # re-create socket (iterface change)
            self._create_socket()
            # error
            raise ConnectionError

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

    def finalize(self):
        # clean up resource called by qtile
        try: self._socket.close()
        except: pass
        # clean up
        base.InLoopPollText.finalize(self)
