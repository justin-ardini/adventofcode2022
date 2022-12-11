from utils import read_day

lines = read_day(2, lambda l: l.split(' '))

WIN = 6
DRAW = 3
LOSE = 0

ROCK = 1
PAPER = 2
SCISSORS = 3

def part1():
  s = 0
  for a, b in pairs:
    if a == 'A' and b == 'X':
      s += ROCK + DRAW
    elif a == 'A' and b == 'Y':
      s += PAPER + WIN
    elif a == 'A' and b == 'Z':
      s += SCISSORS + LOSE
    elif a == 'B' and b == 'X':
      s += ROCK + LOSE
    elif a == 'B' and b == 'Y':
      s += PAPER + DRAW
    elif a == 'B' and b == 'Z':
      s += SCISSORS + WIN
    elif a == 'C' and b == 'X':
      s += ROCK + WIN
    elif a == 'C' and b == 'Y':
      s += PAPER + LOSE
    elif a == 'C' and b == 'Z':
      s += SCISSORS + DRAW
  return s

print(f'Part 1: {part1()}')

def part2():
  s = 0
  for a, b in pairs:
    if a == 'A' and b == 'X':
      s += LOSE + SCISSORS
    elif a == 'A' and b == 'Y':
      s += DRAW + ROCK
    elif a == 'A' and b == 'Z':
      s += WIN + PAPER
    elif a == 'B' and b == 'X':
      s += LOSE + ROCK
    elif a == 'B' and b == 'Y':
      s += DRAW + PAPER
    elif a == 'B' and b == 'Z':
      s += WIN + SCISSORS
    elif a == 'C' and b == 'X':
      s += LOSE + PAPER
    elif a == 'C' and b == 'Y':
      s += DRAW + SCISSORS
    elif a == 'C' and b == 'Z':
      s += WIN + ROCK
  return s

print(f'Part 2: {part2()}')
