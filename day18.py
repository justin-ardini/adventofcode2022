from utils import read_day, int_list
import itertools

SIZE = 21
EMPTY = 0
FILLED = 1

cubes = read_day(18, int_list)

def part1():
  grid = build_grid(cubes)
  return surface_area(grid, cubes)

def build_grid(cubes):
  grid = [[[EMPTY for z in range(SIZE)] for y in range(SIZE)] for x in range(SIZE)]
  for x, y, z in cubes:
    grid[x][y][z] = FILLED
  return grid

def surface_area(grid, cubes):
  area = 0
  for x, y, z in cubes:
    if grid[x-1][y][z] == EMPTY:
      area += 1
    if grid[x+1][y][z] == EMPTY:
      area += 1
    if grid[x][y-1][z] == EMPTY:
      area += 1
    if grid[x][y+1][z] == EMPTY:
      area += 1
    if grid[x][y][z-1] == EMPTY:
      area += 1
    if grid[x][y][z+1] == EMPTY:
      area += 1
  return area

print(f'Part 1: {part1()}')

def part2():
  grid = build_grid(cubes)
  for x, y, z in itertools.product(range(1, SIZE-1), repeat=3):
    if grid[x][y][z] == EMPTY:
      grid = flood(grid, (x, y, z))
  return surface_area(grid, cubes)

def flood(grid, start):
  new_grid = copy_grid(grid)
  q = [start]
  visited = {start}
  while q:
    x, y, z = q.pop()
    new_grid[x][y][z] = FILLED
    neighbors = (
      (x-1,y,z),
      (x+1,y,z),
      (x,y-1,z),
      (x,y+1,z),
      (x,y,z-1),
      (x,y,z+1),
      )
    for n in neighbors:
      if any(x < 0 or x >= SIZE for x in n):
        # Edge reached: this is not an internal point.
        return grid
      xn, yn, zn = n
      if n not in visited and grid[xn][yn][zn] == EMPTY:
        visited.add(n)
        q.append(n)
  return new_grid

def copy_grid(grid):
  return [[c[:] for c in r] for r in grid]

print(f'Part 2: {part2()}')
