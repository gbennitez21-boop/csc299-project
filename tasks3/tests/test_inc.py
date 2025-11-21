import sys
import pathlib

# Add the root of tasks3 (where main.py lives) to Python path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import inc


def test_inc():
    assert inc(5) == 6


def test_inc_negative():
    assert inc(-1) == 0
