from utils import read_day, read_test

LS = 1
CD = 2
MAX_SIZE = 100_000
DISK_SPACE = 70_000_000
UNUSED_SPACE = 30_000_000

def parse_lines(lines):
  i = 0
  out = []
  while i < len(lines):
    line = lines[i]
    parts = line.split(' ')
    if parts[0] == '$':
      if parts[1] == 'cd':
        out.append([CD, parts[2]])
      else:
        sizes = []
        while i + 1 < len(lines) and lines[i + 1][0] != '$':
          i += 1
          ps = lines[i].split(' ')
          sizes.append(ps)
        out.append([LS, sizes])
    i += 1
  return out

lines = read_day(7)
cmds = parse_lines(lines)

def node_size(node):
  if node[3] is None:
    size = 0
    for child in node[2]:
      size += node_size(child)
    return size
  return node[3]

def build_fs(cmds):
  root = ('/', None, [], None)
  curr = root
  for cmd, v in cmds:
    if cmd == CD:
      if v == '..':
        curr = curr[1]
      elif v == '/':
        curr = root
      else:
        for child in curr[2]:
          if child[0] == v:
            curr = child
            break
    elif cmd == LS: # ls
      for a, name in v:
        if a == 'dir':
          node = (name, curr, [], None)
        else:
          node = (name, curr, [], int(a))
        curr[2].append(node)
  return root

def part1():
  root = build_fs(cmds)
  return total_size(root)

def total_size(node):
  tot = 0
  for child in node[2]:
    if child[3] is None:
      s = node_size(child)
      if s <= MAX_SIZE:
        tot += s
      tot += total_size(child)
  return tot

print(f'Part 1: {part1()}')

def part2():
  root = build_fs(cmds)
  root_size = node_size(root)
  min_size = UNUSED_SPACE - (DISK_SPACE - root_size)
  return find_dir(root, min_size)

def find_dir(node, min_size):
  '''Returns the smallest dir with size of at least min_size.'''
  if node[3] is not None:
    return node[3]

  size = node_size(node)
  for child in node[2]:
    s = find_dir(child, min_size)
    if s >= min_size:
      size = min(size, s)
  return size

print(f'Part 2: {part2()}')
