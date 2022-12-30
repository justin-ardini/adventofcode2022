from utils import read_day

inputs = read_day(20, int)

def part1():
  nums = [(i, n) for i, n in enumerate(inputs)]
  nums = mix(nums, inputs)
  return coordinates(nums, inputs)

def mix(nums, inputs):
  l = len(inputs)
  for old_i, n in enumerate(inputs):
    i = nums.index((old_i, n))
    d = n % (l - 1)
    new_i = (i + d) % l
    if new_i < i:
      new_i = (new_i + 1) % l
    del nums[i]
    nums.insert(new_i, (old_i, n))
  return nums

def coordinates(nums, inputs):
  zero_i = inputs.index(0)
  i = nums.index((zero_i, 0))
  return sum(nums[(i + 1000 * j) % len(nums)][1] for j in range(1, 4))

print(f'Part 1: {part1()}')

KEY = 811589153

def part2():
  new_inputs = [KEY * n for n in inputs]
  nums = [(i, n) for i, n in enumerate(new_inputs)]
  for _ in range(10):
    nums = mix(nums, new_inputs)
  return coordinates(nums, new_inputs)

print(f'Part 2: {part2()}')
