from utils import read_day

NUM = 1
ADD = 2
SUB = 3
MULT = 4
DIV = 5
ROOT = 'root'
HUMAN = 'humn'

def parse_line(line):
  parts = line.split(': ')
  name = parts[0]
  job = parts[1]
  if '/' in job:
    t = DIV
    val = job.split(' / ')
  elif '*' in job:
    t = MULT
    val = job.split(' * ')
  elif '+' in job:
    t = ADD
    val = job.split(' + ')
  elif '-' in job:
    t = SUB
    val = job.split(' - ')
  else:
    t = NUM
    val = int(job)
  return (name, t, val)

def build_graph(lines):
  g = {}
  for name, t, val in lines:
    g[name] = (t, val)
  return g

lines = read_day(21, parse_line)
graph = build_graph(lines)

def part1():
  return visit(ROOT, graph[HUMAN][1])

def visit(node, i):
  t, v = graph[node]
  if node == HUMAN:
    return i
  if t == NUM:
    return v
  elif t == ADD:
    return visit(v[0], i) + visit(v[1], i)
  elif t == SUB:
    return visit(v[0], i) - visit(v[1], i)
  elif t == MULT:
    return visit(v[0], i) * visit(v[1], i)
  elif t == DIV:
    return visit(v[0], i) / visit(v[1], i)

print(f'Part 1: {part1()}')

def part2():
  t, v = graph[ROOT]
  target = visit(v[1], 0)
  # NOTE: Lower and upper found by manual inspection!
  lower = 3_000_000_000_000
  upper = 4_000_000_000_000
  i = lower + (upper - lower) // 2
  while True:
    n = visit(v[0], i)
    if n > target:
      lower = i
      i = i + (upper - i) // 2
    elif n < target:
      upper = i
      i = i - (i - lower) // 2
    else:
      return i

print(f'Part 2: {part2()}')
