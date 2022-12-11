from utils import read_day

lines = read_day(3)

def part1():
  s = 0
  pairs = [(l[0:len(l)//2], l[len(l)//2:]) for l in lines]
  for a, b in pairs:
    overlap = [c for c in a if c in b]
    s += get_priority(overlap[0])
  return s

def get_priority(c):
  '''Maps ASCII a-z to 1-26 and A-Z to 27-52.'''
  p = ord(c) - ord('a') + 1
  if p < 1:
    p += 26 + ord('a') - ord('A')
  return p

print(f'Part 1: {part1()}')

def part2():
  s = 0
  for i in range(0, len(lines), 3):
    overlap = [c for c in lines[i] if c in lines[i + 1] and c in lines[i + 2]]
    s += get_priority(overlap[0])
  return s

print(f'Part 2: {part2()}')
