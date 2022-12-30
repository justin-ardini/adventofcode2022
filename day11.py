from utils import read_day, int_list

ADD = 1
MULT = 2
OLD_VALUE = -1

def parse_monkey(lines):
  items = int_list(lines[1].split(':')[1])

  op = lines[2].split(':')[1].split('=')[1].split()
  op[1] = ADD if op[1] == '+' else MULT
  op[2] = OLD_VALUE if op[2] == 'old' else int(op[2])

  test = int(lines[3].split('by')[1])
  if_true = int(lines[4].split('monkey')[1])
  if_false = int(lines[5].split('monkey')[1])

  return {
      'items': items,
      'op': op,
      'test': test,
      'if_true': if_true,
      'if_false': if_false,
      'inspections': 0,
      }

lines = read_day(11)

def part1():
  monkeys = [parse_monkey(lines[i:i+7]) for i in range(0, 56, 7)]
  for _ in range(20):
    for monkey in monkeys:
      run_turn(monkey, monkeys, lambda v: v // 3)
  inspections = sorted([m['inspections'] for m in monkeys], reverse=True)
  return inspections[0] * inspections[1]

def run_turn(monkey, monkeys, calming_fn):
  for item in monkey['items']:
    inspect(item, monkey, monkeys, calming_fn)
  monkey['items'].clear()

def inspect(value, monkey, monkeys, calming_fn):
  op = monkey['op']

  b = value if op[2] == OLD_VALUE else op[2]
  if op[1] == ADD:
    value = value + b
  elif op[1] == MULT:
    value = value * b
  else:
    raise Error('Invalid op')

  value = calming_fn(value)

  if value % monkey['test'] == 0:
    target = monkey['if_true']
  else:
    target = monkey['if_false']

  monkeys[target]['items'].append(value)
  monkey['inspections'] += 1

print(f'Part 1: {part1()}')


def part2():
  monkeys = [parse_monkey(lines[i:i+7]) for i in range(0, 56, 7)]
  # Compute lcm to keep worry value small enough (assumes prime numbers)
  lcm = 1
  for monkey in monkeys:
    lcm *= monkey['test']

  for _ in range(10000):
    for monkey in monkeys:
      run_turn(monkey, monkeys, lambda v: v % lcm)
  inspections = sorted([m['inspections'] for m in monkeys], reverse=True)
  return inspections[0] * inspections[1]

print(f'Part 2: {part2()}')
