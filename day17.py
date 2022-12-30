from utils import read_day

EMPTY = 0
FILLED = 1

COLS = 7
ROWS = 100_000

def new_grid():
  return [[FILLED if r == 0 else EMPTY] * COLS for r in range(ROWS)]

jets = read_day(17)[0]

def part1():
  grid = new_grid()
  return run_sim(2022)

def run_sim(n, j=0, offset=0):
  grid = new_grid()
  for i in range(n):
     rock = add_rock(grid, (i+offset) % 5)
     while True:
       rock = push_rock(grid, rock, j)
       j = (j + 1) % len(jets)
       rock = drop_rock(grid, rock)
       if not rock:
         break
  return first_empty_row(grid) - 1

def push_rock(grid, rock, j):
  d = 1 if jets[j] == '>' else -1
  for r, c in rock:
    if c + d < 0 or c + d >= COLS:
      return rock
    if (r, c+d) not in rock and grid[r][c+d] == FILLED:
      return rock
  for r, c in rock:
    grid[r][c] = EMPTY
  for r, c in rock:
    grid[r][c+d] = FILLED
  return [(r, c+d) for r, c in rock]

def drop_rock(grid, rock):
  for r, c in rock:
    if (r-1, c) not in rock and grid[r-1][c] == FILLED:
      return None
  for r, c in rock:
    grid[r][c] = EMPTY
  for r, c in rock:
    grid[r-1][c] = FILLED
  return [(r-1, c) for r, c in rock]

def add_rock(grid, i):
  r = first_empty_row(grid) + 3
  c = 2
  rock = []
  if i == 0: # Horiz line
    rock.append((r, c))
    rock.append((r, c + 1))
    rock.append((r, c + 2))
    rock.append((r, c + 3))
    pass
  elif i == 1: # Plus
    rock.append((r + 1, c))
    rock.append((r + 1, c + 1))
    rock.append((r + 1, c + 2))
    rock.append((r, c + 1))
    rock.append((r + 2, c + 1))
    pass
  elif i == 2: # Backwards L
    rock.append((r, c))
    rock.append((r, c + 1))
    rock.append((r, c + 2))
    rock.append((r + 1, c + 2))
    rock.append((r + 2, c + 2))
  elif i == 3: # Vert line
    rock.append((r, c))
    rock.append((r + 1, c))
    rock.append((r + 2, c))
    rock.append((r + 3, c))
  else: # Square
    rock.append((r, c))
    rock.append((r + 1, c))
    rock.append((r, c + 1))
    rock.append((r + 1, c + 1))
  for r, c in rock:
    grid[r][c] = FILLED
  return rock

def first_empty_row(grid):
  for r in range(ROWS):
    empty = True
    for c in range(COLS):
      if grid[r][c] == FILLED:
        empty = False
        break
    if empty:
      return r

print(f'Part 1: {part1()}')

def part2():
  start, cycle, j = find_cycle()
  offset = start % 5
  height = run_sim(cycle, j, offset)
  num_cycles = 1_000_000_000_000 // cycle
  remainder = 1_000_000_000_000 % cycle
  return height * num_cycles + run_sim(start) + run_sim(remainder - start, j, offset)

def find_cycle():
  grid = new_grid()
  j = 0
  mappings = {}
  for i in range(1_000_000):
     r = first_empty_row(grid) - 1
     if all((grid[r][c] == FILLED for c in range(COLS))):
       if (j, i%5) in mappings:
         start = mappings[(j, i%5)]
         return start, i - start, j
       mappings[(j, i % 5)] = i
     rock = add_rock(grid, i % 5)
     while True:
       rock = push_rock(grid, rock, j)
       j = (j + 1) % len(jets)
       rock = drop_rock(grid, rock)
       if not rock:
         break
  return -1

print(f'Part 2: {part2()}')
