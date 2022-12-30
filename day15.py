from utils import read_day, read_inputs, Vec2d

def parse_line(line):
  a, b = line.split(':')
  a = a.split('at')[1]
  b = b.split('at')[1]
  xs, ys = a.split(',')
  xs = xs.split('=')[1]
  ys = ys.split('=')[1]
  xb, yb = b.split(',')
  xb = xb.split('=')[1]
  yb = yb.split('=')[1]
  return Vec2d(int(xs), int(ys)), Vec2d(int(xb), int(yb))

lines = read_day(15, parse_line)

def part1():
  y_val = 2000000
  triples = []
  x_min = 1000000
  x_max = 0
  beacons = set()
  for sensor, beacon in lines:
    beacons.add(beacon)
    x_min = min(x_min, sensor.x)
    x_min = min(x_min, beacon.x)
    x_max = max(x_max, sensor.x)
    x_max = max(x_max, beacon.x)
    distance = sensor.distance(beacon)
    triples.append((sensor, beacon, distance))
  count = 0
  for x in range(x_min - 3000000, x_max + 3000000):
    b = Vec2d(x, y_val)
    for sensor, beacon, distance in triples:
      dist = sensor.distance(b)
      if dist <= distance and b not in beacons:
        count += 1
        break
  return count

print(f'Part 1: {part1()}')

def part2():
  triples = []
  x_min = 1000000
  x_max = 0
  beacons = set()
  for sensor, beacon in lines:
    beacons.add(beacon)
    x_min = min(x_min, sensor.x)
    x_min = min(x_min, beacon.x)
    x_max = max(x_max, sensor.x)
    x_max = max(x_max, beacon.x)
    distance = sensor.distance(beacon)
    triples.append((sensor, beacon, distance))
  count = 0
  for i, (sensor, beacon, distance) in enumerate(triples):
    for x in range(max(0, sensor.x - distance - 1), min(4_000_001, sensor.x + distance + 2)):
      xd = abs(sensor.x - x)
      yd = distance - xd + 1
      for y in (sensor.y-yd, sensor.y+yd):
        if y < 0 or y > 4_000_000:
          continue
        b = Vec2d(x, y)
        dist = sensor.distance(b)
        if dist == distance + 1:
          bad = False
          for i2, (s2, _, d2) in enumerate(triples):
            if i != i2:
              if s2.distance(b) <= d2:
                bad = True
                break
          if not bad:
            return x * 4000000 + y
  return -1

print(f'Part 2: {part2()}')
