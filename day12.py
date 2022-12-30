from utils import read_day
import heapq

def build_graph(lines):
  graph = {}
  start = None
  end = None
  for i, row in enumerate(lines):
    for j, c in enumerate(row):
      if c == 'S':
        start = (i, j)
      elif c == 'E':
        end = (i, j)
      neighbors = []
      if i > 0:
        neighbors.append((i-1, j))
      if i < len(lines) - 1:
        neighbors.append((i+1, j))
      if j > 0:
        neighbors.append((i, j-1))
      if j < len(row) - 1:
        neighbors.append((i,j+1))
      graph[(i, j)] = [(x, y) for x, y in neighbors if get_val(lines[x][y]) <= get_val(c) + 1]
  return graph, start, end

def get_val(c):
  if c == 'S':
    return ord('a')
  if c == 'E':
    return ord('z')
  return ord(c)

lines = read_day(12)
graph, start, end = build_graph(lines)

def part1():
  return a_star(graph, start, end, {})

def a_star(graph, start, end, costs):
  q = []
  heapq.heappush(q, (distance(start, end), start, 0))
  while q:
    cost, curr, steps = heapq.heappop(q)
    if curr == end:
      return steps
    for n in graph[curr]:
      old_steps = costs.get(n)
      new_steps = steps + 1
      if n not in costs or new_steps < old_steps:
        costs[n] = new_steps
        heapq.heappush(q, (new_steps + distance(n, end), n, new_steps))

  return 1_000_000

def distance(a, b):
  return sum(abs(x - y) for x, y in zip(a, b))

print(f'Part 1: {part1()}')

def part2():
  min_steps = 1_000_000
  costs = {}
  for start in gen_starts(lines):
    costs[start] = 0
    min_steps = min(min_steps, a_star(graph, start, end, costs))
  return min_steps

def gen_starts(lines):
  for i, row in enumerate(lines):
    for j, c in enumerate(row):
      if c == 'a':
        yield (i, j)

print(f'Part 2: {part2()}')
