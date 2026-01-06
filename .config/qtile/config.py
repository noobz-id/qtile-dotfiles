# custom lib
import hooks
from groups import GROUPS
from keybinds import KEYS, MOUSE_KEYS
from layouts import LAYOUTS, FLOATING_LAYOUT
from screens import SCREEN, WIDGET_DEFAULT

# option qtile config
dgroups_key_binder = None
dgroups_app_rules = [] # type: list
follow_mouse_focus = True
bring_front_click = False
auto_full_screen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screen = True
floats_kept_above = True
cursor_warp = False
auto_minimize = True
idle_inhibitors = [] # type: list
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

