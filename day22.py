from utils import read_day, Vec2d
import re

NULL = 0
OPEN = 1
WALL = 2

UP = Vec2d(-1, 0)
DOWN = Vec2d(1, 0)
LEFT = Vec2d(0, -1)
RIGHT = Vec2d(0, 1)

def parse_grid(lines):
  cols = max(len(l) for l in lines)
  grid = [[NULL] * cols for _ in range(len(lines))]
  for r, row in enumerate(lines):
    for c, val in enumerate(row):
      grid[r][c] = NULL if val == ' ' else OPEN if val == '.' else WALL
  return grid

def parse_path(path):
  parts = re.split(r'(L|R)', path)
  return [int(c) if c not in ('L', 'R') else c for c in parts]

data = read_day(22, sep='\n\n')
grid = parse_grid(data[0].split('\n'))
path = parse_path(data[1])

def part1():
  d = RIGHT
  pos = Vec2d(0, grid[0].index(OPEN))
  for step in path:
    if step == 'L':
      d = turn_left(d)
    elif step == 'R':
      d = turn_right(d)
    else:
      for _ in range(step):
        pos = move(grid, pos, d)
  return 1000 * (pos.x + 1) + 4 * (pos.y + 1) + dir_value(d)

def turn_left(d):
  return Vec2d(-d.y, d.x)

def turn_right(d):
  return Vec2d(d.y, -d.x)

def move(grid, pos, d):
  n = Vec2d((pos.x + d.x) % len(grid), (pos.y + d.y) % len(grid[0]))
  while grid[n.x][n.y] == NULL:
    n = Vec2d((n.x + d.x) % len(grid), (n.y + d.y) % len(grid[0]))
  if grid[n.x][n.y] == OPEN:
    return n
  else:
    return pos

def dir_value(d):
  if d == RIGHT:
    return 0
  if d == DOWN:
    return 1
  if d == LEFT:
    return 2
  if d == UP:
    return 3
  raise Exception('Invalid direction')

print(f'Part 1: {part1()}')

SIZE = len(grid[0]) // 3

def part2():
  sides = side_sets(grid)
  d = RIGHT
  pos = Vec2d(0, grid[0].index(OPEN))
  # sanity_check(grid, sides)
  for step in path:
    if step == 'L':
      d = turn_left(d)
    elif step == 'R':
      d = turn_right(d)
    else:
      for _ in range(step):
        pos,d = move3d(grid, pos, d, sides)
  return 1000 * (pos.x + 1) + 4 * (pos.y + 1) + dir_value(d)

def sanity_check(grid, sides):
  blank_grid = [[NULL if grid[r][c] == NULL else OPEN for c in range(len(row))] for r, row in enumerate(grid)]
  l = len(blank_grid[0]) // 3
  correct = 0
  wrongs = set()
  starts = sides.keys()
  for start in starts:
    for d_start in (UP, DOWN, LEFT, RIGHT):
      pos = start
      d = d_start
      for _ in range(l * 4):
        pos, d = move3d(blank_grid, pos, d, sides)
      if pos == start and d == d_start:
        correct += 1
      else:
        wrongs.add((pos, d_start, d))
  print(wrongs)

def side_sets(grid):
  l = len(grid[0]) // 3
  sides = {}
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      if r in range(l) and c in range(l, 2*l):
        sides[Vec2d(r, c)] = 1
      elif r in range(l) and c in range(2*l, len(row)):
        sides[Vec2d(r, c)] = 2
      elif r in range(l, 2*l) and c in range(l, 2*l):
        sides[Vec2d(r, c)] = 3
      elif r in range(2*l, 3*l) and c in range(l):
        sides[Vec2d(r, c)] = 4
      elif r in range(2*l, 3*l) and c in range(l, 2*l):
        sides[Vec2d(r, c)] = 5
      elif r in range(3*l, len(grid)) and c in range(l):
        sides[Vec2d(r, c)] = 6
      elif v != NULL:
        raise Exception('Invalid')
  return sides

def move3d(grid, pos, d, sides):
  '''Hacky movement along cube surface, not a generalized solution!'''
  l = len(grid[0]) // 3
  n = Vec2d((pos.x + d.x) % len(grid), (pos.y + d.y) % len(grid[0]))
  side = sides[pos]
  n_side = sides.get(n)
  nd = d
  # Move within side
  if side == n_side:
    if grid[n.x][n.y] == WALL:
      n = pos
  else:
    # 1 -> Other
    if side == 1:
      if d == UP:
        n = Vec2d(3*l + pos.y % l, pos.x % l)
        nd = RIGHT
        assert sides[n] == 6 # 1 -> 6
      elif d == DOWN:
        assert sides[n] == 3 # 1 -> 3
      elif d == LEFT:
        n = Vec2d(2*l + l-1 - (pos.x % l), (pos.y % l))
        nd = RIGHT
        assert sides[n] == 4 # 1 -> 4
      elif d == RIGHT:
        assert sides[n] == 2 # 1 -> 2
    # 2 -> Other
    elif side == 2:
      if d == UP:
        n = Vec2d(3*l + l-1 - (pos.x % l), pos.y % l)
        nd = UP
        assert sides[n] == 6 # 2 -> 6
      elif d == DOWN:
        n = Vec2d(l + (pos.y % l), l + (pos.x % l))
        nd = LEFT
        assert sides[n] == 3 # 2 -> 3
      elif d == LEFT:
        pass # 2 -> 1
      elif d == RIGHT:
        n = Vec2d(2*l + l-1 - (pos.x % l), l + (pos.y % l))
        nd = LEFT
        assert sides[n] == 5 # 2 -> 5
    # 3 -> Other
    elif side == 3:
      if d == UP:
        assert sides[n] == 1 # 3 -> 1
      elif d == DOWN:
        assert sides[n] == 5 # 3 -> 5
      elif d == LEFT:
        n = Vec2d(2*l + (pos.y % l), (pos.x % l))
        nd = DOWN
        assert sides[n] == 4 # 3 -> 4
      elif d == RIGHT:
        n = Vec2d(pos.y % l, 2*l + (pos.x % l))
        nd = UP
        assert sides[n] == 2 # 3 -> 2
    # 4 -> Other
    elif side == 4:
      if d == UP:
        n = Vec2d(l + (pos.y % l), l + (pos.x % l))
        nd = RIGHT
        assert sides[n] == 3
      elif d == DOWN:
        assert sides[n] == 6
      elif d == LEFT:
        n = Vec2d(l-1 - (pos.x % l), l + (pos.y % l)) # 1 -> 4
        nd = RIGHT
        assert sides[n] == 1
      elif d == RIGHT:
        assert sides[n] == 5
    # 5 -> Other
    elif side == 5:
      if d == UP:
        assert sides[n] == 3
      elif d == DOWN:
        n = Vec2d(3*l + (pos.y % l), (pos.x % l))
        nd = LEFT
        assert sides[n] == 6
      elif d == LEFT:
        assert sides[n] == 4
      elif d == RIGHT:
        n = Vec2d(l-1 - (pos.x % l), 2*l + (pos.y % l))
        nd = LEFT
        assert sides[n] == 2
    # 6 -> Other
    elif side == 6:
      if d == UP:
        assert sides[n] == 4
      elif d == DOWN:
        n = Vec2d(l-1 - pos.x % l, 2*l + (pos.y % l))
        nd = DOWN
        assert sides[n] == 2
      elif d == LEFT:
        n = Vec2d(pos.y % l, l + (pos.x % l))
        nd = DOWN
        assert sides[n] == 1
      elif d == RIGHT:
        n = Vec2d(2*l + (pos.y % l), l + (pos.x % l))
        nd = UP
        assert sides[n] == 5

  if grid[n.x][n.y] == OPEN:
    return n, nd
  else:
    return pos, d

print(f'Part 2: {part2()}')
