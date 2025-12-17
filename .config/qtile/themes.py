from abc import ABC, abstractmethod


# Base theme
class BaseTheme(ABC):
    # color map
    BACKGROUND: str
    FOREGROUND: str
    BLACK: str
    RED: str
    GREEN: str
    YELLOW: str
    BLUE: str
    MAGENTA: str
    CYAN: str
    WHITE: str

    @classmethod
    @abstractmethod
    def accent(cls) -> str:
        raise NotImplementedError("accent color not implemented")


# one dark theme
class _OneDarkTheme(BaseTheme):
    BACKGROUND = "1e2127"
    FOREGROUND = "abb2bf"
    BLACK = "5c6370"
    RED = "e06c75"
    GREEN = "98c379"
    YELLOW = "d19a66"
    BLUE = "61afef"
    MAGENTA = "c678dd"
    CYAN = "65b6c2"
    WHITE = "828791"

    @classmethod
    def accent(cls) -> str:
        return cls.CYAN


# export
# set theme here
THEME: BaseTheme = _OneDarkTheme()
