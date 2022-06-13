import re

def genall(rules, id):
  if isinstance(rules[id], list):
    ret = set()
    for subrule in rules[id]:
      if len(subrule) == 1:
        ret |= genall(rules, subrule[0])
      else:
        part0 = genall(rules, subrule[0])
        part1 = genall(rules, subrule[1])
        for i in part0:
          for j in part1:
            ret.add(i + j)
    return ret
  else:
    return set(rules[id])

with open("data/day19.txt") as f:
  rules = {}
  for line in f:
    line = line.rstrip()
    if line == "":
      break

    id, content = line.split(": ")
    if '"' in content:
      rules[int(id)] = content[1]
    else:
      subrules = content.split(" | ")
      groups = [re.findall(r"(\d+)", s) for s in subrules]
      rules[int(id)] = [[int(y) for y in x] for x in groups]

  v0 = genall(rules, 0)
  v42 = genall(rules, 42)
  v31 = genall(rules, 31)
  chunk_len = len(next(iter(v42)))
  print("(v42, v31, chunk_len) =", (len(v42), len(v31), chunk_len))
  print("v42 & v31 =", v42 & v31)

  part1, part2 = 0, 0
  for line in f:
    line = line.rstrip()

    if line in v0:
      part1 += 1

    def chunk_type(c):
      if c in v42:
        return 42
      elif c in v31:
        return 31
    chunks = [chunk_type(line[i:i+chunk_len]) for i in range(0, len(line), chunk_len)]
    n42 = chunks.count(42)
    n31 = chunks.count(31)
    if n42 > n31 and n31 > 0 and chunks[0:n42] == [42] * n42:
      part2 += 1

  print("part1 =", part1)
  print("part2 =", part2)
