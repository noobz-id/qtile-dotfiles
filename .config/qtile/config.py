import subprocess

from libqtile import hook

# custom lib
from groups import GROUPS
from keybinds import KEYS, MOUSE_KEYS
from layouts import LAYOUTS
from screens import SCREEN, WIDGET_DEFAULT

# init qtile config
follow_mouse_focus = True
auto_full_screen = True
focus_on_window_activation = "smart"
reconfigure_screen = True
floats_kept_above = True
cursor_warp = False
auto_minimize = False
wmname = "LG3D"  # hack old java gui app

# custom qtile config
keys = KEYS
mouse = MOUSE_KEYS
layouts = LAYOUTS
screens = SCREEN
groups = GROUPS
widget_defaults = WIDGET_DEFAULT
extension_defaults = WIDGET_DEFAULT


# run once at start
@hook.subscribe.startup_once
def startup_once():
    # background call
    subprocess.Popen(["lxsession"])


# run every start including restart
@hook.subscribe.startup
def startup():
    # foreground call
    subprocess.run(["xsetroot", "-cursor_name", "left_ptr"])
    subprocess.run(["xmodmap", "-e", "keysym Menu = Super_R"])


# run every new window spawned
@hook.subscribe.client_new
def dialogs(window):
    # check is dialog like type to floating window
    if window.window.get_wm_type() == "dialog" or window.window.get_wm_transient_for():
        window.floating = True
