from utils import read_day
import heapq

OPEN = 0
WALL = 1
UP = 2
RIGHT = 3
DOWN = 4
LEFT = 5

def parse_line(line):
  return [parse_char(c) for c in line]

def parse_char(c):
  if c == '.':
    return OPEN
  elif c == '#':
    return WALL
  elif c == '^':
    return UP
  elif c == '>':
    return RIGHT
  elif c == 'v':
    return DOWN
  elif c == '<':
    return LEFT
  raise Error('Invalid char')

grid = read_day(24, parse_line)

def part1():
  min_to_blizzard = simulate_blizzards(grid)
  start = (0, 1)
  end = (len(grid) - 1, len(grid[0]) - 2)
  return a_star(min_to_blizzard, start, end)

def simulate_blizzards(grid):
  blizzards = get_blizzards(grid)
  rows = len(grid) - 2
  cols = len(grid[0]) - 2
  min_to_blizzard = [blizzards]
  while True:
    blizzards = get_next_blizzards(blizzards, grid)
    if min_to_blizzard[0] == blizzards:
      return min_to_blizzard
    min_to_blizzard.append(blizzards)

def get_blizzards(grid):
  rows = len(grid) - 2
  cols = len(grid[0]) - 2
  blizzards = {}
  for r, row in enumerate(grid):
    for c, b in enumerate(row):
      if b in (UP, DOWN, LEFT, RIGHT):
        blizzards[(r, c)] = [b]
  return blizzards

def get_next_blizzards(blizzards, grid):
  rows = len(grid) - 2
  cols = len(grid[0]) - 2
  next_blizzards = {}
  for (r, c), blizz in blizzards.items():
    for b in blizz:
      if b == UP:
        if r == 1:
          pos = (r + rows - 1, c)
        else:
          pos = (r - 1, c)
      elif b == DOWN:
        if r == rows:
          pos = (1, c)
        else:
          pos = (r + 1, c)
      elif b == LEFT:
        if c == 1:
          pos = (r, c + cols - 1)
        else:
          pos = (r, c - 1)
      elif b == RIGHT:
        if c == cols:
          pos = (r, 1)
        else:
          pos = (r, c + 1)
      next_blizzards.setdefault(pos, []).append(b)
  return next_blizzards

def a_star(min_to_blizzard, start, end, start_mins = 0):
  l = len(min_to_blizzard)
  q = []
  max_pos = (max(start[0], end[0]) - 1, max(start[1], end[1]))
  heapq.heappush(q, (distance(start, end), start, start_mins))
  min_time = 10000
  bests = {}
  while q:
    _, pos, mins = heapq.heappop(q)
    if pos == end:
      return mins
    new_mins = mins + 1
    for n in open_positions(pos, min_to_blizzard[new_mins % l], max_pos):
      old_mins = bests.get((n, new_mins % l), 100_000)
      if new_mins < old_mins:
        bests[(n, new_mins % l)] = new_mins
        heapq.heappush(q, (new_mins + distance(n, end), n, new_mins))
  return min_time

def distance(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def open_positions(pos, blizzards, max_pos):
  positions = [pos]
  if pos[0] > 1 or pos == (1, 1):
    positions.append((pos[0]-1, pos[1]))
  if pos[0] < max_pos[0] or pos == max_pos:
    positions.append((pos[0]+1, pos[1]))
  if pos[0] <= max_pos[0] and pos[1] > 1:
    positions.append((pos[0], pos[1]-1))
  if pos[0] > 0 and pos[1] != max_pos[1]:
    positions.append((pos[0], pos[1]+1))
  return (p for p in positions if p not in blizzards)

print(f'Part 1: {part1()}')

def part2():
  min_to_blizzard = simulate_blizzards(grid)
  start = (0, 1)
  end = (len(grid) - 1, len(grid[0]) - 2)
  mins = a_star(min_to_blizzard, start, end, 0)
  mins = a_star(min_to_blizzard, end, start, mins)
  return a_star(min_to_blizzard, start, end, mins)

print(f'Part 2: {part2()}')
