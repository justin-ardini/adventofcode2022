from utils import read_day

data = read_day(6)[0]

def part1():
  return find_marker(4)

def find_marker(n):
  '''Returns the number of characters processed to find the n-character marker.'''
  for i in range(0, len(data) - n):
    if len(set(data[i:i+n])) == n:
      return i + n
  return -1

print(f'Part 1: {part1()}')

def part2():
  return find_marker(14)

print(f'Part 2: {part2()}')
