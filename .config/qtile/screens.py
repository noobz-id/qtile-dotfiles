from libqtile import bar, widget
from libqtile.config import Screen

# custom lib
from themes import THEME, FONT


def _separator():
    return widget.Sep(background=THEME.BACKGROUND, foreground=THEME.BACKGROUND)


# bar
_top_bar_widgets = [
    #
    # Left panel
    #
    widget.GroupBox(
        highlight_method="text",
        this_current_screen_border=THEME.GREEN,
        active=THEME.MAGENTA,
        inactive=THEME.BLACK,
        borderWidth=0,
        padding_x=0,
        padding_y=0,
        margin_x=0,
    ),
    _separator(),
    widget.CurrentLayout(background=THEME.BACKGROUND, foreground=THEME.RED),
    _separator(),
    widget.WindowName(
        max_chars=65, background=THEME.BACKGROUND, foreground=THEME.WHITE
    ),
    #
    # Right panel
    #
    widget.Net(
        format="net: {up:.0f}{up_suffix}/{down:.0f}{down_suffix}",
        background=THEME.BACKGROUND,
        foreground=THEME.WHITE,
    ),
    _separator(),
    widget.CPU(
        format="cpu: {load_percent:.0f}%",
        background=THEME.BACKGROUND,
        foreground=THEME.RED,
    ),
    _separator(),
    widget.Memory(
        measure_mem="G",
        format="mem: {MemUsed:.1f}/{MemTotal:.1f}GB",
        background=THEME.BACKGROUND,
        foreground=THEME.YELLOW,
    ),
    _separator(),
    widget.Battery(
        charge_char="char",
        discharge_char="bat",
        empty_char="emp",
        full_char="full",
        not_charging_char="acp",
        format="{char}: {percent:2.0%}",
        battery=0,
        background=THEME.BACKGROUND,
        foreground=THEME.GREEN,
        low_foreground=THEME.RED,
        update_interval=1,
    ),
    _separator(),
    widget.Clock(
        format="%a %d-%b-%Y %I:%M %p",
        background=THEME.BACKGROUND,
        foreground=THEME.BLUE,
    ),
    _separator(),
    widget.Systray(background=THEME.BACKGROUND, icon_size=15, padding=3),
]

# export

# default widget font size
WIDGET_DEFAULT = dict(
    font=FONT,
    fontsize=12,
    padding=3,
)

# main screen, currently i have 1 screen only
SCREEN = [
    Screen(top=bar.Bar(widgets=_top_bar_widgets, size=20, background=THEME.BACKGROUND))
]
