from utils import read_day

def parse_line(line):
  return [parse_char(c) for c in line]

def parse_char(c):
  if c == '0':
    return 0
  elif c == '1':
    return 1
  elif c == '2':
    return 2
  elif c == '-':
    return -1
  elif c == '=':
    return -2

lines = read_day(25, parse_line)

def part1():
  s = sum(to_decimal(l) for l in lines)
  return to_snafu(s)

def to_decimal(digits):
  return sum(n * 5**i for i, n in enumerate(digits[::-1]))

def to_snafu(n):
  to_digit = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
  digits = []
  while n != 0:
    d = (n + 2) % 5 - 2
    n = (n - d) // 5
    digits += to_digit[d]
  return ''.join(digits[::-1])

print(f'Part 1: {part1()}')
