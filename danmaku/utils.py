"""Helper functions."""

from enum import IntEnum
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
    """Check if the object is in screen boundary"""
    if vy < 0 and y <= 0:
        return False
    if vy > 0 and y >= height:
        return False
    if vx < 0 and x <= 0:
        return False
    if vx > 0 and x >= width:
        return False
    return True


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # pylint: disable=protected-access
        base_path = Path(sys._MEIPASS)  # type: ignore
    except AttributeError:
        base_path = Path(__file__).parent.parent

    return str(base_path / "assets" / relative_path)


def constrain(
    value: int | float, min_value: int | float, max_value: int | float
) -> int | float:
    """Constrain value between min_value and max_value."""
    return max(min(value, max_value), min_value)


class Direction(IntEnum):
    """Direction enum."""

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    STATIC = 4


# def str_to_stage(stage_str: str) -> Stage: ...


# def str_to_level(level_str: str) -> Level:
#     """Convert level string to level object."""
#     ...
