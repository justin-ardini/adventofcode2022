from utils import read_day
import math
import queue

MINS = 24
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

def parse_line(line):
  parts = line.split('.')
  ore_cost = int(parts[0].split('costs')[1].split(' ')[1])
  clay_cost = int(parts[1].split('costs')[1].split(' ')[1])
  obsidian_costs = parts[2].split('costs')[1].split(' ')
  obsidian_costs = (int(obsidian_costs[1]), int(obsidian_costs[4]))
  geode_costs = parts[3].split('costs')[1].split(' ')
  geode_costs = (int(geode_costs[1]), int(geode_costs[4]))
  return [(ore_cost, 0, 0, 0),
      (clay_cost, 0, 0, 0),
      (obsidian_costs[0], obsidian_costs[1], 0, 0),
      (geode_costs[0], 0, geode_costs[1], 0)]

blueprints = read_day(19, parse_line)

def part1():
  quality = 0
  for i, blueprint in enumerate(blueprints):
    geodes = get_geodes(blueprint)
    quality += (i + 1) * geodes
  return quality

def get_geodes(blueprint):
  q = queue.Queue()
  max_geodes = 0
  max_costs = tuple(max(b[i] for b in blueprint) for i in range(4))
  bests = {}
  # mins, resources, bots, next bot
  q.put((0, (0, 0, 0, 0), (1, 0, 0, 0), ORE))
  q.put((0, (0, 0, 0, 0), (1, 0, 0, 0), CLAY))
  while not q.empty():
    mins, resources, bots, next_bot = q.get()
    elapsed = buy(resources, bots, blueprint[next_bot])
    new_mins = mins + elapsed
    if new_mins > MINS:
      geodes = resources[GEODE] + (MINS - mins) * bots[GEODE]
      max_geodes = max(max_geodes, geodes)
      continue
    new_resources = tuple(r - c + b * elapsed for r, b, c in zip(resources, bots, blueprint[next_bot]))
    new_bots = tuple(v + 1 if i == next_bot else v for i, v in enumerate(bots))
    old_mins = bests.get(new_bots, MINS)
    if old_mins < new_mins:
      continue
    bests[new_bots] = new_mins
    if new_bots[OBSIDIAN] != 0:
      q.put((new_mins, new_resources, new_bots, GEODE))
    if new_bots[CLAY] != 0 and should_build(MINS- new_mins, new_resources, new_bots, max_costs, OBSIDIAN):
      q.put((new_mins, new_resources, new_bots, OBSIDIAN))
    if should_build(MINS - new_mins, new_resources, new_bots, max_costs, CLAY):
      q.put((new_mins, new_resources, new_bots, CLAY))
    if should_build(MINS - new_mins, new_resources, new_bots, max_costs, ORE):
      q.put((new_mins, new_resources, new_bots, ORE))
  return max_geodes

def should_build(mins, resources, bots, costs, bot_type):
  '''True if the total cost for the resource is greater than the current production.'''
  r = resources[bot_type]
  b = bots[bot_type]
  c = costs[bot_type]
  return mins * c > mins * b + r

def buy(resources, bots, costs):
  '''Spend time to buy a robot'''
  # Amount to buy: cost - resources
  # Time to buy: amount / bot
  deficits = (c - r for c, r in zip(costs, resources))
  return 1 + max(math.ceil(d / b) if d > 0 else 0 for d, b in zip(deficits, bots))

print(f'Part 1: {part1()}')

MINS = 32

def part2():
  prod = 1
  for i in range(3):
    prod *= get_geodes(blueprints[i])
  return prod

print(f'Part 2: {part2()}')
