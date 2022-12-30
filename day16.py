from utils import read_day
from itertools import combinations
import heapq
import queue

START = 'AA'
MAX_MINS = 30

def parse_line(line):
  parts = line.split(';')
  a = parts[0].split(' ')
  valves = parts[1].split(' ')[5:]
  valves = [v[:2] for v in valves]
  name = a[1]
  flow_rate = int(a[-1].split('=')[1])
  return (name, flow_rate, valves)

def build_graph(lines):
  graph = {}
  nonzero_valves = set()
  # Start with immediate neighbors.
  for name, flow_rate, valves in lines:
    graph[name] = (flow_rate, valves)
    if flow_rate != 0:
      nonzero_valves.add(name)
  # Replace with distances to non-zero valves.
  new_graph = {}
  for name, flow_rate, _ in lines:
    if flow_rate != 0 or name == START:
      new_graph[name] = (flow_rate, find_distances(graph, name, nonzero_valves))
  return new_graph

def find_distances(graph, start, nonzero_valves):
  q = queue.Queue()
  q.put((start, 0))
  distances = {start: 0}
  outputs = {}
  while not q.empty():
    name, mins = q.get()
    if name in nonzero_valves and name != start:
      outputs[name] = mins
    _, neighbors = graph[name]
    for n in neighbors:
      n_mins = mins + 1
      if n_mins < distances.get(n, 1000):
        distances[n] = n_mins
        q.put((n, n_mins))
  return outputs


lines = read_day(16, parse_line)
graph = build_graph(lines)

def part1():
  return find_max_flow(graph, START)

def find_max_flow(graph, start):
  q = []
  heapq.heappush(q, (0, 0, start, [], 0))
  max_flow = 0
  while q:
    _, flow, curr, visited, mins = heapq.heappop(q)
    if mins == MAX_MINS:
      max_flow = max(max_flow, flow)
      continue
    if len(visited) == len(graph) - 1:
      new_flow = flow + (MAX_MINS - mins) * tick(graph, visited)
      max_flow = max(max_flow, new_flow)
      continue
    for n, distance in graph[curr][1].items():
      if n not in visited:
        if mins + distance < MAX_MINS:
          new_flow = flow + (distance + 1) * tick(graph, visited)
          new_visited = visited[:]
          new_visited.append(n)
          heapq.heappush(q, (-new_flow, new_flow, n, new_visited, mins + distance + 1))
        else:
          new_flow = flow + (MAX_MINS - mins) * tick(graph, visited)
          max_flow = max(max_flow, new_flow)

  return max_flow

def tick(graph, on):
  return sum(graph[v][0] for v in on)

print(f'Part 1: {part1()}')

def part2():
  l = len(graph)
  min_size = len(graph) // 2 - 1
  max_size = len(graph) // 2 + 1
  max_flow = 0
  valves = [v for v in graph.keys() if v != START]
  for s in range(min_size, max_size + 1):
    for me, elephant in valve_splits(graph, valves, s):
      flow = find_max_flow2(me, START, 26) + find_max_flow2(elephant, START, 26)
      max_flow = max(max_flow, flow)
  return max_flow

def valve_splits(graph, valves, size):
  '''Splits the valves into two groups and returns each subgraph.'''
  for combo in combinations(valves, size):
    me = {START: graph[START]}
    elephant = {START: graph[START]}
    for v in valves:
      if v in combo:
        me[v] = graph[v]
      else:
        elephant[v] = graph[v]
    for k, v in me.items():
      me[k] = (v[0], {k:x for k,x in v[1].items() if k in me})
    for k, v in elephant.items():
      elephant[k] = (v[0], {k:x for k,x in v[1].items() if k in elephant})
    yield me, elephant

def find_max_flow2(graph, start, max_mins):
  q = []
  heapq.heappush(q, (0, 0, start, [], 0))
  max_flow = 0
  while q:
    _, flow, curr, visited, mins = heapq.heappop(q)
    if mins == max_mins:
      max_flow = max(max_flow, flow)
      continue
    if len(visited) == len(graph) - 1:
      new_flow = flow + (max_mins - mins) * tick(graph, visited)
      max_flow = max(max_flow, new_flow)
      continue
    for n, distance in graph[curr][1].items():
      if n not in visited:
        if mins + distance < max_mins:
          new_flow = flow + (distance + 1) * tick(graph, visited)
          new_visited = visited[:]
          new_visited.append(n)
          heapq.heappush(q, (-new_flow, new_flow, n, new_visited, mins + distance + 1))
        else:
          new_flow = flow + (max_mins - mins) * tick(graph, visited)
          max_flow = max(max_flow, new_flow)

  return max_flow

print(f'Part 2: {part2()}')
