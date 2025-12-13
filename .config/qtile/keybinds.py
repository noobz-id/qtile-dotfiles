import os

# qtile lib
from libqtile.config import Click, Drag, Key
from libqtile.lazy import lazy

# custom lib
import groups

# Default
_mod = "mod4"
_terminal = "alacritty"

# special key
_left = "h"
_right = "l"
_down = "j"
_up = "k"
_shift = "shift"
_enter = "Return"
_ctrl = "control"
_space = "space"

# combination
_mod_shift = [_mod, _shift]
_mod_ctrl = [_mod, _ctrl]


# path
_home_path = os.path.expanduser("~")


# move window to prev group
@lazy.function
def window_to_prev_group(qtile):
    cur_idx = qtile.groups.index(qtile.current_group)
    prev_idx = (cur_idx - 1) % len(qtile.groups)
    group = qtile.groups[prev_idx].name
    # exec
    qtile.current_window.togroup(group, switch_group=True)


# move window to next group
@lazy.function
def window_to_next_group(qtile):
    cur_idx = qtile.groups.index(qtile.current_group)
    next_idx = (cur_idx + 1) % len(qtile.groups)
    group = qtile.groups[next_idx].name
    # exec
    qtile.current_window.togroup(group, switch_group=True)


# kill all active windows
@lazy.function
def kill_all_windows(qtile):
    for window in qtile.current_group.windows:
        window.kill()


# Key bindings

_hardware_keys = [
    # Volume
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume 0 -5%"),
        desc="volume down",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume 0 +5%"),
        desc="volume up",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute 0 toggle"),
        desc="volume mute toggle",
    ),
    # Display
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +5%"),
        desc="brightness up",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 5%-"),
        desc="brightness down",
    ),
]

_action_keys = [
    Key([_mod], _left, lazy.layout.left(), desc="switch window left"),
    Key([_mod], _right, lazy.layout.right(), desc="switch window right"),
    Key([_mod], _down, lazy.layout.down(), desc="switch window down"),
    Key([_mod], _up, lazy.layout.up(), desc="switch window up"),
    Key([_mod], "f", lazy.window.toggle_floating(), desc="floating window"),
    Key([_mod], "minus", lazy.screen.prev_group(), desc="switch to prev group"),
    Key([_mod], "equal", lazy.screen.next_group(), desc="switch to next group"),
    Key(
        [_mod], _space, lazy.window.toggle_fullscreen(), desc="toggle window fullscreen"
    ),
    Key(_mod_shift, _left, lazy.layout.shuffle_left(), desc="shuffle window to left"),
    Key(
        _mod_shift, _right, lazy.layout.shuffle_right(), desc="shuffle window to right"
    ),
    Key(_mod_shift, _down, lazy.layout.shuffle_down(), desc="shuffle window to down"),
    Key(_mod_shift, _up, lazy.layout.shuffle_up(), desc="shuffle window to up"),
    Key(_mod_shift, "minus", window_to_prev_group(), desc="move window to prev group"),
    Key(_mod_shift, "equal", window_to_next_group(), desc="move window to next group"),
    Key(_mod_shift, _space, lazy.next_layout(), desc="change to next layout"),
    Key(_mod_shift, "c", lazy.window.kill(), desc="kill focused window"),
    Key(_mod_shift, "a", kill_all_windows(), desc="kill all windows"),
    Key(_mod_ctrl, "q", lazy.shutdown(), desc="kill qtile or logout"),
    Key(_mod_ctrl, "r", lazy.reload_config(), desc="reload qtile config"),
]

_spawn_keys = [
    Key([_mod], _enter, lazy.spawn(_terminal), desc="Launch terminal"),
    Key(
        [_mod], "p", lazy.spawn("rofi -show drun -show-icons"), desc="launch rofi menu"
    ),
    Key(_mod_shift, "p", lazy.spawn("rofi-pass"), desc="launch rofi password manager"),
    Key(
        [_mod],
        "Tab",
        lazy.spawn(
            "rofi -modi \"clipboard:greenclip print\" -show clipboard -run-command '{cmd}'"
        ),
        desc="launch rofi clipboard manager",
    ),
    Key(
        [_mod],
        "Print",
        lazy.spawn(
            f"scrot {_home_path}/Pictures/screenshot/%Y-%m-%d-%T-screenshot.png"
        ),
        desc="take screenshot",
    ),
]

_group_keys = [
    key
    for group in groups.GROUPS
    for key in (
        Key(
            [_mod],
            group.name,
            lazy.group[group.name].toscreen(),
            desc=f"switch to group {group.name}",
        ),
        Key(
            _mod_shift,
            group.name,
            lazy.window.togroup(group.name, switch_group=True),
            desc=f"move focused window to group {group.name}",
        ),
    )
]

# mouse

_mouse_keys = [
    Drag(
        [_mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [_mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([_mod], "Button2", lazy.window.bring_to_front()),
]

# export
KEYS = _hardware_keys + _action_keys + _spawn_keys + _group_keys
MOUSE_KEYS = _mouse_keys
