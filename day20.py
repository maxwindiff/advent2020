import math
import re
from typing import List, NamedTuple

class Tile(NamedTuple):
  id: int
  img: List[str]
  borders: List[str]

def borders(img):
  # top, right, bottom, left
  return [img[0], "".join([l[-1] for l in img]), img[-1], "".join([l[0] for l in img])]

def matches(border, t2):
  for j in range(4):
    if border == t2.borders[j] or border == t2.borders[j][::-1]:
      return True
  return None

def graph(tiles):
  g = {t.id: set() for t in tiles}
  for t1 in tiles:
    for t2 in tiles:
      if t1.id == t2.id:
        continue
      for i in range(4):
        if matches(t1.borders[i], t2):
          g[t1.id].add(t2.id)
  return g

def part1(g):
  return math.prod(id for id, conn in g.items() if len(conn) == 2)

def transformed(tile):
  tiles = [tile]
  img = tile.img
  for _ in range(3):
    img = ["".join(row) for row in zip(*img[::-1])]
    tiles.append(Tile(tile.id, img, borders(img)))
  for i in range(4):
    img = [row[::-1] for row in tiles[i].img]
    tiles.append(Tile(tile.id, img, borders(img)))
  return tiles

def merge(tiles, g):
  tiles = {t.id: t for t in tiles}
  top_left = next(id for id, conn in g.items() if len(conn) == 2)

  for starting in transformed(tiles[top_left])[:4]:
    placement = [[]]

    current = starting
    placement[-1].append(current)
    placed = 1

    while True:
      for neighbor in g[current.id]:
        for candidate in transformed(tiles[neighbor]):
          # Match right border of current tile with left border of candidate
          if current.borders[1] == candidate.borders[3]:
            current = candidate
            placement[-1].append(current)
            placed += 1
            break
      if len(g[current.id]) == 2:  # Reached right edge
        break

    # Failed to place even the first row, meaning starting orientation is wrong
    if current.id == starting.id:
      continue

    # TODO: place second row, etc
    print(placement)

tiles = []
with open("data/day20a.txt") as f:
  id = 0
  img = []
  for line in f:
    line = line.rstrip()
    if "Tile" in line:
      id = int(re.match(r"Tile (\d+):", line)[1])
    elif line == "":
      tiles.append(Tile(id, img, borders(img)))
      img = []
    else:
      img.append(line)
  if len(img) > 0:
    tiles.append(Tile(id, img, borders(img)))

g = graph(tiles)
print(part1(g))
print(merge(tiles, g))
