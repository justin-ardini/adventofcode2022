from utils import read_day

def parse_calories(lines):
  """Returns a list of list of calories, with each internal list representing an elf."""
  out = []
  curr = []
  for line in lines:
    if line:
      curr.append(int(line))
    else:
      out.append(curr)
      curr = []
  return out

all_calories = parse_calories(read_day(1))

def part1():
  return max(sum(l) for l in all_calories)

print(f'Part 1: {part1()}')

def part2():
  s = sorted([sum(l) for l in all_calories], reverse=True)
  return s[0] + s[1] + s[2]

print(f'Part 2: {part2()}')
