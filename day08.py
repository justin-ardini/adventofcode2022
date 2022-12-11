from utils import read_day, int_grid

heights = read_day(8, int_grid)

def part1():
  total = 0
  for r, row in enumerate(heights):
    for c, _ in enumerate(row):
      total += is_visible(heights, r, c)
  return total

def is_visible(heights, r, c):
  h = heights[r][c]
  row = heights[r]
  return all(heights[i][c] < h for i in range(0, r)) or \
      all(heights[i][c] < h for i in range(r + 1, len(heights))) or \
      all(heights[r][j] < h for j in range(0, c)) or \
      all(heights[r][j] < h for j in range(c + 1, len(row)))

print(f'Part 1: {part1()}')

def part2():
  max_score = 0
  for r, row in enumerate(heights):
    for c, _ in enumerate(row):
      s = scenic_score(heights, r, c)
      max_score = max(max_score, s)
  return max_score

def scenic_score(heights, r, c):
  h = heights[r][c]
  row = heights[r]

  a = 0
  for i in range(r-1, -1, -1):
    a += 1
    if heights[i][c] >= h:
      break
  b = 0
  for i in range(r+1, len(heights)):
    b += 1
    if heights[i][c] >= h:
      break
  e = 0
  for j in range(c-1, -1, -1):
    e += 1
    if heights[r][j] >= h:
      break
  d = 0
  for j in range(c+1, len(row)):
    d += 1
    if heights[r][j] >= h:
      break
  return a * b * e * d

print(f'Part 2: {part2()}')
