from utils import read_day

def parse_line(line):
  '''Returns a list of sets of ints.'''
  parts = line.split(',')
  out = []
  for part in parts:
    nums = [int(c) for c in part.split('-')]
    out.append({n for n in range(nums[0], nums[1] + 1)})
  return out

all_ranges = read_day(4, parse_line)

def part1():
  return sum(a >= b or a < b for a, b in all_ranges)

print(f'Part 1: {part1()}')

def part2():
  return sum(len(a & b) > 0 for a, b in all_ranges)

print(f'Part 2: {part2()}')
