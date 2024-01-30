import sys
from pathlib import Path


def not_in_border(
    x: int | float,
    y: int | float,
    vx: int | float,
    vy: int | float,
    width: int | float,
    height: int | float,
) -> bool:
    if vy < 0 and y <= 0:
        return False
    elif vy > 0 and y >= height:
        return False
    elif vx < 0 and x <= 0:
        return False
    elif vx > 0 and x >= width:
        return False
    else:
        return True


def resource_path(relative_path) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(__file__).parent.parent

    return str(base_path / "assets" / relative_path)
