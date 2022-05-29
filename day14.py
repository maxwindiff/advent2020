from typing import NamedTuple
import re
from itertools import chain, combinations

class Mask(NamedTuple):
  mask0: int
  mask1: int
  maskX: int
  posXs: 'list[int]'

class Cmd(NamedTuple):
  addr: int
  val: int

class Session(NamedTuple):
  mask: Mask
  cmds: 'list[Cmd]'

def to_mask(str):
  mask0, mask1, maskX = 0, 0, 0
  posX, posXs = (1<<35), []
  for c in str:
    if c == '0':
      mask0 |= 1
    elif c == '1':
      mask1 |= 1
    elif c == 'X':
      maskX |= 1
      posXs.append(posX)
    mask0 <<= 1
    mask1 <<= 1
    maskX <<= 1
    posX >>= 1
  return Mask(mask0 >> 1, mask1 >> 1, maskX >> 1, posXs)

def load(filename):
  with open(filename) as f:
    sessions = []
    for line in f:
      if line[0:4] == "mask":
        sessions.append(Session(to_mask(line[7:-1]), []))
      else:
        (addr, val) = re.findall(r"\d+", line)
        sessions[-1].cmds.append(Cmd(int(addr), int(val)))
    return sessions

def masking(val, mask):
  return val & (mask.mask0) | mask.mask1

def part1(sessions):
  memory = {}
  for s in sessions:
    for cmd in s.cmds:
      memory[cmd.addr] = masking(cmd.val, s.mask)
  return sum(v for v in memory.values())

def floating(posXs):
  powerset = chain.from_iterable(combinations(posXs, r) for r in range(len(posXs)+1))
  return (sum(xs) for xs in powerset)

def part2(sessions):
  memory = {}
  for s in sessions:
    for cmd in s.cmds:
      for x in floating(s.mask.posXs):
        memory[masking(cmd.addr, s.mask) & (~s.mask.maskX) | x] = cmd.val
  return sum(v for v in memory.values())

sessions = load("data/day14.txt")
print("part1 =", part1(sessions))
print("part2 =", part2(sessions))
