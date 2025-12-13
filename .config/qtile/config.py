import subprocess

from libqtile import hook

# custom lib
from groups import GROUPS
from keybinds import KEYS, MOUSE_KEYS
from layouts import LAYOUTS, FLOATING_LAYOUT
from screens import SCREEN, WIDGET_DEFAULT

# init qtile config
follow_mouse_focus = True
auto_full_screen = True
focus_on_window_activation = "smart"
reconfigure_screen = True
floats_kept_above = True
cursor_warp = False
auto_minimize = True
wmname = "LG3D"  # hack old java gui app

# custom qtile config
keys = KEYS
mouse = MOUSE_KEYS
layouts = LAYOUTS
screens = SCREEN
groups = GROUPS
floating_layout = FLOATING_LAYOUT
widget_defaults = WIDGET_DEFAULT
extension_defaults = WIDGET_DEFAULT


# run once at start
@hook.subscribe.startup_once
def on_init_once():
    # background call
    subprocess.Popen(["lxsession"])


# run every start including restart
@hook.subscribe.startup
def on_start():
    # foreground call
    subprocess.run(["xsetroot", "-cursor_name", "left_ptr"])
    subprocess.run(["xmodmap", "-e", "keysym Menu = Super_R"])


# run every new window spawned
@hook.subscribe.client_new
def on_spawn(window):
    # check is dialog like type to floating window
    if window.window.get_wm_type() == "dialog" or window.window.get_wm_transient_for():
        # set to floating
        window.floating = True

# run every float window detected
@hook.subscribe.float_change
def on_floating_changed(window):
    # check is floating window
    if window.floating:
        # get screen
        screen = window.qtile.current_screen
        # Center calculation
        x = screen.x + (screen.width - window.width) // 2
        y = screen.y + (screen.height - window.height) // 2
        # Apply
        window.x = x
        window.y = y
        # Optional: Also set size if needed
        window.width = min(window.width, screen.width - 100)
        window.height = min(window.height, screen.height - 100)
