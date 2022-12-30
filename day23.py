from utils import read_day, bit_grid, get_neighbors

OPEN = 0
ELF = 1
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
STEPS = 10

input_grid = read_day(23, bit_grid)

def part1():
  grid = input_grid
  dirs = [NORTH, SOUTH, WEST, EAST]
  for i in range(STEPS):
    moves = next_moves(grid, dirs, i)
    grid = step(grid, moves)
  return len(grid) * len(grid[0]) - count_elves(grid)

def count_elves(grid):
  return sum(sum(c == ELF for c in r) for r in grid)

def next_moves(grid, dirs, i):
  moves = {}
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      if v == ELF:
        move = next_move(grid, r, c, dirs, i)
        if move in moves:
          moves[move].append((r, c))
        else:
          moves[move] = [(r, c)]
  all_moves = []
  for k, l in moves.items():
    if len(l) == 1:
      all_moves.append(k)
    else:
      all_moves += l
  return all_moves

def next_move(grid, r, c, dirs, i):
  nr = len(grid)
  nc = len(grid[0])
  if all(grid[r][c] == OPEN for r, c in neighbors(grid, (r, c))):
    return (r, c)
  for j in range(4):
    d = dirs[(i + j) % 4]
    if d == NORTH:
      if r == 0:
        return (-1, c)
      if all((
          c == 0 or grid[r-1][c-1] == OPEN,
          grid[r-1][c] == OPEN,
          c == nc - 1 or grid[r-1][c+1]== OPEN)):
        return (r-1, c)
    elif d == SOUTH:
      if r == nr - 1:
        return (nr, c)
      if all((
          c == 0 or grid[r+1][c-1] == OPEN,
          grid[r+1][c] == OPEN,
          c == nc - 1 or grid[r+1][c+1] == OPEN)):
        return (r+1, c)
    elif d == WEST:
      if c == 0:
        return (r, -1)
      if all((
          r == 0 or grid[r-1][c-1] == OPEN,
          grid[r][c-1] == OPEN,
          r == nr -1 or grid[r+1][c-1] == OPEN)):
        return (r, c-1)
    elif d == EAST:
      if c == nc - 1:
        return (r, nc)
      if all((
          r == 0 or grid[r-1][c+1] == OPEN,
          grid[r][c+1] == OPEN,
          r == nr - 1 or grid[r+1][c+1] == OPEN)):
        return (r, c+1)
  return (r, c)

def step(grid, moves):
  nr = len(grid)
  nc = len(grid[0])
  rmin = min(m[0] for m in moves)
  rmax = max(m[0] for m in moves)
  cmin = min(m[1] for m in moves)
  cmax = max(m[1] for m in moves)
  grid = [[OPEN] * (cmax - cmin + 1) for r in range (rmax - rmin + 1)]
  ro = -rmin
  co = -cmin
  for r, c in moves:
    grid[r+ro][c+co] = ELF
  return grid

def neighbors(grid, cell):
  return get_neighbors(grid, cell, (len(grid), len(grid[0])))

print(f'Part 1: {part1()}')

def part2():
  grid = input_grid
  dirs = [NORTH, SOUTH, WEST, EAST]
  for i in range(1_000_000):
    moves = next_moves(grid, dirs, i)
    next_grid = step(grid, moves)
    if next_grid == grid:
      return i + 1
    grid = next_grid
  return -1

print(f'Part 2: {part2()}')
