from utils import read_day, Vec2d

LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'

def parse_line(line):
  parts = line.split(' ')
  return (parts[0], int(parts[1]))

moves = read_day(9, parse_line)

def part1():
  head = Vec2d(0, 0)
  tail = Vec2d(0, 0)
  visited = {tail}
  for direction, distance in moves:
    for _ in range(distance):
      head = move_head(direction, head)
      tail = move_tail(head, tail)
      visited.add(tail)
  return len(visited)

def move_head(direction, head):
  if direction == LEFT:
    return head - Vec2d(1, 0)
  elif direction == RIGHT:
    return head + Vec2d(1, 0)
  elif direction == UP:
    return head + Vec2d(0, 1)
  elif direction == DOWN:
    return head - Vec2d(0, 1)
  raise Error('Invalid direction')

def move_tail(head, tail):
  dx = head.x - tail.x
  dy = head.y - tail.y

  # Vertical
  if dx == 0 and abs(dy) == 2:
      return tail + Vec2d(0, dy // 2)

  # Horizontal
  if abs(dx) == 2 and dy == 0:
      return tail + Vec2d(dx // 2, 0)

  # Diagonal
  if abs(dx) == 1 and abs(dy) == 2:
    return tail + Vec2d(dx, dy // 2)
  if abs(dx) == 2 and abs(dy) == 1:
    return tail + Vec2d(dx // 2, dy)
  if abs(dx) == 2 and abs(dy) == 2:
    return tail + Vec2d(dx // 2, dy // 2)

  return tail


print(f'Part 1: {part1()}')

def part2():
  knots = [Vec2d(0, 0)] * 10
  visited = {knots[-1]}
  for direction, distance in moves:
    for _ in range(distance):
      knots[0] = move_head(direction, knots[0])
      for i in range(1, len(knots)):
        knots[i] = move_tail(knots[i - 1], knots[i])
      visited.add(knots[-1])
  return len(visited)

print(f'Part 2: {part2()}')
