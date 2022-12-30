from functools import reduce
from typing import Union
import itertools
import operator

Number = Union[float, int]

def read_day(day: int, map_fn=str, sep = '\n') -> list:
  return read_inputs(f'day{str(day).zfill(2)}.txt', map_fn, sep)

def read_inputs(f: str, map_fn=str, sep = '\n') -> list:
  """Applies map_fn to each item, defaults to 1 item per line."""
  with open(f'inputs/{f}') as f:
    parts = f.read().rstrip().split(sep)
    return list(map(map_fn, parts))

# --- Start input parsers ---
def char_grid(s: str) -> list:
  return [c for c in s]

def str_list(s: str, sep = ',') -> list:
  return [x for x in s.split(sep)]

def int_grid(s: str) -> list:
  return [int(c) for c in s]

def int_list(s: str, sep = ',') -> list:
  return [int(c) for c in s.split(sep)]

def bit_grid(s: str, on = '#') -> list:
  return [1 if c == on else 0 for c in s]

def vec_pair(s: str, sep = ','):
  return Vec2d(*(int(c) for c in s.split(sep)))

# --- End input parsers ---

def prod(iterable):
  """Product of numbers: use like sum()."""
  return reduce(operator.mul, iterable, 1)

def clamp(n, n_min, n_max):
  return max(min(n, n_max), n_min)

def bits_to_dec(bits):
  """Converts iterable of bits to decimal number."""
  out = 0
  for bit in bits:
    out = (out << 1) | bit
  return out

def copy_grid(grid):
  """Returns a copy of a 2D grid."""
  return [r[:] for r in grid]

def get_neighbors(grid, cell, dimensions):
  '''Returns all neighbors (including diagonals) of an N-dimensional grid cell.'''
  for c in itertools.product(*(range(i-1, i+2) for i in cell)):
    if c != cell and all(i >= 0 and i < s for i, s in zip(c, dimensions)):
      yield c

# 2D vector
class Vec2d:
  def __init__(self, x: Number, y: Number):
    self.x = x
    self.y = y

  def __add__(self, v):
    return Vec2d(self.x + v.x, self.y + v.y)

  def add(self, v):
    return self + v

  def __sub__(self, v):
    return Vec2d(self.x - v.x, self.y - v.y)

  def sub(self, v):
    return self - v

  def __neg__(self):
    return Vec2d(-self.x, -self.y)

  def __mul__(self, s: Number):
    return Vec2d(self.x * s, self.y * s)

  def mul(self, s: Number):
    return self * s

  # Manhattan distance
  def distance(self, v):
    return abs(self.x - v.x) + abs(self.y - v.y)

  def __eq__(self, v):
    return self.x == v.x and self.y == v.y

  def __hash__(self):
    return hash((self.x, self.y))

  def __str__(self):
    return f'({self.x},{self.y})'

  def __repr__(self):
    return f'Vec2d({self.x},{self.y})'
