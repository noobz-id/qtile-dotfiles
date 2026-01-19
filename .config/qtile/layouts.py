from libqtile import layout

# custom lib
from themes import THEME

_default = {
    "border_width": 2,
    "margin": 2,
    "border_focus": THEME.accent(),
    "border_normal": THEME.BACKGROUND,
}

# export
LAYOUTS = [
    layout.MonadTall(name="T", **_default),
    layout.Matrix(name="M", **_default),
]

FLOATING_LAYOUT = layout.Floating(
    name="F",
    float_rules=[*layout.Floating.default_float_rules],
    border_focus=THEME.accent(),
    border_normal=THEME.BACKGROUND,
    border_width=2
)


