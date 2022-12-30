from utils import read_day
from functools import cmp_to_key
import ast

def parse_line(line):
  return ast.literal_eval(line) if line else None

def to_pairs(lines):
  pairs = []
  for i in range(0, len(lines), 3):
    pairs.append((lines[i], lines[i+1]))
  return pairs

lines = read_day(13, parse_line)

def part1():
  pairs = to_pairs(lines)
  s = 0
  for i, (a, b) in enumerate(pairs):
    if compare(a, b) < 0:
      s += i + 1
  return s

def compare(left, right):
  '''Returns negative if left < right, 0 if equal, positive if left > right.'''
  if isinstance(left, int) and isinstance(right, int):
    return left - right
  if isinstance(left, int):
    left = [left]
  if isinstance(right, int):
    right = [right]

  for l, r in zip(left, right):
    c = compare(l, r)
    if c != 0:
      return c
  return len(left) - len(right)

print(f'Part 1: {part1()}')

def part2():
  l = [l for l in lines if l is not None]
  x = [[2]]
  y = [[6]]
  l.append(x)
  l.append(y)
  l.sort(key=cmp_to_key(compare))
  return (l.index(x) + 1) * (l.index(y) + 1)

print(f'Part 2: {part2()}')
