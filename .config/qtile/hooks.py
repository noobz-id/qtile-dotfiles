import subprocess

from libqtile import hook, qtile

from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupText

# custom lib
from themes import THEME, FONT


# run once at start
@hook.subscribe.startup_once
def on_init():
    # launch session manager in background
    subprocess.Popen(["lxsession"])


# run every start including restart
@hook.subscribe.startup
def on_start():
    # set cursor theme
    subprocess.run(["xsetroot", "-cursor_name", "left_ptr"])
    # map menu key to Super_R
    subprocess.run(["xmodmap", "-e", "keysym Menu = Super_R"])


# run every new window spawned
@hook.subscribe.client_new
def on_spawn(window):
    # check is dialog like type to floating window
    if window.window.get_wm_type() == "dialog" or window.window.get_wm_transient_for():
        # set to floating
        window.floating = True


# run every group/workspace changed/switched
@hook.subscribe.setgroup
def on_group_changed():
    # show centered popup to tell where group/workspace is
    PopupRelativeLayout(
        qtile,
        controls = [
            PopupText(
                text = qtile.current_group.name,
                pos_x = 0,
                pos_y = 0,
                width = 1,
                height = 1,
                h_align = "center",
                v_align = "middle",
                font = FONT,
                fontsize = 80,
                foreground = THEME.FOREGROUND,
            ),
        ],
        width = 100,
        height = 100,
        background = THEME.BACKGROUND,
        initial_focus = None,
        hide_on_timeout = 1,
    ).show(centered = True)


