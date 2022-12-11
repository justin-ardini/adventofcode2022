from utils import read_day

def parse_stacks(lines):
  n = 9
  start = 1
  inc = 4
  return [[l[i] for l in lines[::-1] if l[i] != ' '] for i in range(start, start + inc * n, inc)]

def parse_cmd(line):
  '''Returns a list of (n, start_index, end_index) tuples.'''
  parts = line.split(' ')
  n = int(parts[1])
  start = int(parts[3]) - 1
  end = int(parts[5]) - 1
  return (n, start, end)

lines = read_day(5)
stacks = parse_stacks(lines[:8])
cmds = [parse_cmd(l) for l in lines[10:]]

def part1():
  for n, start, end in cmds:
    for _ in range(n):
      stacks[end].append(stacks[start].pop())
  return ''.join(s[-1] for s in stacks)

print(f'Part 1: {part1()}')
stacks = parse_stacks(lines[:8])

def part2():
  for n, start, end in cmds:
    s = []
    stacks[end] += stacks[start][-n:]
    del stacks[start][-n:]
  return ''.join(s[-1] for s in stacks)

print(f'Part 2: {part2()}')
