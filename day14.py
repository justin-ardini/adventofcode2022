from utils import read_day, vec_pair, Vec2d

def parse_line(line):
  coords = line.split('->')
  return [vec_pair(c) for c in coords]

lines = read_day(14, parse_line)

def part1():
  # draw lines
  occupied = set()
  for coords in lines:
    for i in range(len(coords) - 1):
      a = coords[i]
      b = coords[i + 1]
      if a.x == b.x:
        dy = 1 if a.y < b.y else -1
        for y in range(a.y, b.y + dy, dy):
          occupied.add(Vec2d(a.x, y))
      else:
        dx = 1 if a.x < b.x else -1
        for x in range(a.x, b.x + dx, dx):
          occupied.add(Vec2d(x, a.y))

  for i in range(100_000):
    start = Vec2d(500, 0)
    pos = drop(occupied, start)
    if pos:
      occupied.add(pos)
    else:
      return i
  return -1

def drop(occupied, start, floor_fn=lambda v: False):
  prev = start
  for i in range(1000):
    # down
    step = prev + Vec2d(0, 1)
    if step in occupied or floor_fn(step):
      # down left
      step.x -= 1
      if step in occupied or floor_fn(step):
        # down right
        step.x += 2
        if step in occupied or floor_fn(step):
          return prev
    prev = step
  return None

print(f'Part 1: {part1()}')

def part2():
  # draw lines
  max_y = 0
  occupied = set()
  for coords in lines:
    for i in range(len(coords) - 1):
      a = coords[i]
      b = coords[i + 1]
      max_y = max(max_y, a.y)
      max_y = max(max_y, b.y)
      if a.x == b.x:
        dy = 1 if a.y < b.y else -1
        for y in range(a.y, b.y + dy, dy):
          occupied.add(Vec2d(a.x, y))
      else:
        dx = 1 if a.x < b.x else -1
        for x in range(a.x, b.x + dx, dx):
          occupied.add(Vec2d(x, a.y))

  floor_fn = lambda v: v.y == max_y + 2
  for i in range(100_000):
    start = Vec2d(500, 0)
    pos = drop(occupied, start, floor_fn)
    if pos == start:
      return i + 1
    if pos:
      occupied.add(pos)
  return -1

print(f'Part 2: {part2()}')
