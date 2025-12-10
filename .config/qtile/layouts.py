from libqtile import layout

from themes import THEME

_default = {
    "border_width": 2,
    "margin": 2,
    "border_focus": THEME.accent(),
    "border_normal": THEME.BACKGROUND,
}

# export
LAYOUTS = [
    layout.MonadTall(**_default),
    layout.Max(**_default),
    layout.Floating(
        border_focus=THEME.accent(),
        border_normal=THEME.BACKGROUND,
        border_width=2,
    ),
]
