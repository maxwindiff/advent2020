import copy

with open("data/day17a.txt") as f:
  input = f.readlines()
  input = [l.rstrip() for l in input]

sx = len(input)
sy = max(len(l) for l in input)
sz = 1
sw = 1
tx, ty, tz, tw = sx+14, sy+14, sz+14, sw+14

def neighbors(s, x, y, z, w):
  count = 0
  for l in range(w-1, w+2):
    for k in range(z-1, z+2):
      for j in range(y-1, y+2):
        for i in range(x-1, x+2):
          if s[l][k][j][i] == '#':
            count += 1
  if s[w][z][y][x] == '#':
    count -= 1
  return count

def sim(part):
  state = [[[['.' for _ in range(tx)] for _ in range(ty)] for _ in range(tz)] for _ in range(tw)]
  for w in range(1):
    for z in range(1):
      for y in range(sy):
        for x in range(sx):
          state[w+7][z+7][y+7][x+7] = input[y][x]

  for c in range(1, 7):
    next = [[[['.' for _ in range(tx)] for _ in range(ty)] for _ in range(tz)] for _ in range(tw)]
    for w in range(7-c, 7+sw+c) if part == 2 else range(7, 8):
      for z in range(7-c, 7+sz+c):
        for y in range(7-c, 7+sy+c):
          for x in range(7-c, 7+sx+c):
            pop = neighbors(state, x, y, z, w)
            if state[w][z][y][x] == '#':
              if pop in (2, 3):
                next[w][z][y][x] = '#'
            else:
              if pop == 3:
                next[w][z][y][x] = '#'
    state = copy.deepcopy(next)

  total = 0
  for w in range(0, tw):
    for z in range(0, tz):
      for y in range(0, ty):
        for x in range(0, tx):
          if state[w][z][y][x] == '#':
            total += 1
  return total

print("part1 =", sim(1))
print("part2 =", sim(2))
