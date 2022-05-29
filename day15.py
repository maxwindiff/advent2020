def part(input, turns):
  last_seen = {}

  for i, num in enumerate(input, start=1):
    last_seen[num] = i

  # assume inputs are unique, so next spoken number is always 0
  spoken = 0
  next_spoken = 0

  for turn in range(len(input)+1, turns):
    if spoken in last_seen:
      next_spoken = turn - last_seen[spoken]
    else:
      next_spoken = 0
    last_seen[spoken] = turn
    spoken = next_spoken

  return spoken

with open("data/day15.txt") as f:
  line = f.readline().rstrip()
  input = [int(x) for x in line.split(",")]

print(part([0, 3, 6], 2020))
print("part1 =", part(input, 2020))
print("part2 = ", part(input, 30000000))
