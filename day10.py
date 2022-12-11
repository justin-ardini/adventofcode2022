from utils import read_day

ADDX = 1
NOOP = 2

def parse_line(line):
  parts = line.split(' ')
  if parts[0] == 'noop':
    return NOOP, 0
  elif parts[0] == 'addx':
    return ADDX, int(parts[1])

cmds = read_day(10, parse_line)

def part1():
  i = 0
  x = 1
  signal = 0
  while i < 240:
    for cmd, v in cmds:
      signal += signal_strength(x, i)
      if cmd == ADDX:
        i += 1
        signal += signal_strength(x, i)
        x += v
      i += 1
  return signal

def signal_strength(x, i):
  cycle = i + 1
  if cycle % 40 == 20:
    return x * cycle
  return 0

print(f'Part 1: {part1()}')

def part2():
  i = 0
  x = 1
  pixels = []
  while i < 240:
    for cmd, v in cmds:
      pixels.append(get_pixel(x, i))
      if cmd == ADDX:
        i += 1
        pixels.append(get_pixel(x, i))
        x += v
      i += 1
  draw(pixels)

def get_pixel(x, i):
  pos = i % 40
  if abs(pos - x) <= 1:
    return '#'
  else:
    return ' '

def draw(pixels):
  for i in range(240):
    print(pixels[i], end='')
    if i % 40 == 39:
      print('')

print('Part 2:')
part2()
