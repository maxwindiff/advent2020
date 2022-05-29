import re
from typing import NamedTuple
from pprint import pp

class Field(NamedTuple):
  name: str
  r1: range
  r2: range

def allowed(num, field):
  return num in field.r1 or num in field.r2

def part1(fields, tickets):
  error = 0
  for t in tickets:
    for num in t:
      if not any(allowed(num, f) for f in fields):
        error += num
  return error

def valid(fields, ticket):
  for num in ticket:
    if not any(allowed(num, f) for f in fields):
      return False
  return True

def part2(fields, your, nearby):
  tickets = [n for n in nearby if valid(fields, n)]
  tickets.append(your)

  indices = set(range(0, len(your)))
  field_names = {f.name for f in fields}
  neighbors = {
    i: set(f.name for f in fields if all(allowed(ticket[i], f) for ticket in tickets))
    for i in indices
  }

  MAX_DIST = 9999
  dist = {x: MAX_DIST for x in indices}
  match = {x: None for x in indices | field_names}

  def bfs():
    q = []
    for i in indices:
      if match[i] is None:
        dist[i] = 0
        q.append(i)
      else:
        dist[i] = MAX_DIST

    target_dist = MAX_DIST
    while len(q) > 0:
      i = q.pop(0)
      if dist[i] < target_dist:
        for j in neighbors[i]:
          k = match[j]
          if k is None:
            target_dist = dist[i] + 1
          elif dist[k] == MAX_DIST:
            dist[k] = dist[i] + 1
            q.append(k)

    return target_dist < MAX_DIST

  def dfs(i):
    for j in neighbors[i]:
      k = match[j]
      if k is None or (dist[k] == dist[i] + 1 and dfs(k)):
        match[i] = j
        match[j] = i
        return True

    dist[i] = MAX_DIST
    return False

  for _ in range(0, len(your)):
    bfs()
    for i in indices:
      if match[i] is None:
        dfs(i)

  ans = 1
  for f in field_names:
    if f.split()[0] == 'departure':
      ans *= your[match[f]]
  return ans

def load(filename):
  fields = []
  your = []
  nearby = []

  with open(filename) as f:
    while f:
      line = f.readline().rstrip()
      if line == "":
        break
      match = re.match(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line)
      name = match.group(1)
      s1, e1, s2, e2 = (int(x) for x in match.groups()[1:])
      fields.append(Field(name, range(s1, e1+1), range(s2, e2+1)))

    f.readline()
    your = [int(x) for x in f.readline().rstrip().split(",")]

    f.readline()
    f.readline()
    while f:
      line = f.readline().rstrip()
      if line == "":
        break
      nearby.append([int(x) for x in line.split(",")])

  return fields, your, nearby


fields, your, nearby = load("data/day16.txt")
print("part1 =", part1(fields, nearby))
print("part2 =", part2(fields, your, nearby))
