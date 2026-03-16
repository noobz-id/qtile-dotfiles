# lib
import subprocess
import time
import psutil

net_data = {
    "last_time": time.time(),
    "last_recv": 0,
    "last_sent": 0,
}

def _bytes_format(size):
    # convert to (B, KB, MB, GB, T) human readable bytes
    for unit in ['B', 'K', 'M', 'G']:
        if size < 1024:
            # ok
            return f"{int(size)}{unit}" if unit == 'B' else f"{size:.1f}{unit}" 
        # 
        size /= 1024
    # fallback
    return f"{size:.1f}T"

# export
def active_network_meter():
    # cache last data
    global net_data
    try:
        # get active interface
        interface = subprocess.check_output(
            "ip route get 8.8.8.8 2>/dev/null | grep -Po '(?<=dev )\\S+'", 
            shell=True
        ).decode("utf-8").strip()
        # get interface list
        io = psutil.net_io_counters(pernic=True).get(interface)
        # get stat
        recv = io.bytes_recv
        sent = io.bytes_sent
        # time stamp
        now = time.time()
        elapsed = now - net_data["last_time"]
        # calculate speed
        down_speed = (recv - net_data["last_recv"]) / elapsed
        up_speed = (sent - net_data["last_sent"]) / elapsed
        # update cache
        net_data.update({
            "last_time": now,
            "last_recv": recv,
            "last_sent": sent
        })
        # format
        down_fmt = _bytes_format(down_speed)
        up_fmt = _bytes_format(up_speed)
        #
        return f"{interface}: {up_fmt}/{down_fmt}"
    except Exception:
        return "offline"
