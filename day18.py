import re
from functools import reduce
from itertools import chain, groupby
from typing import NamedTuple

class Expr(NamedTuple):
  op: str
  val: int
  elems: 'list[Expr]'

  def __repr__(self):
    if self.elems:
      return "{" + reduce(lambda x, y: f"{x} {self.op} {y}", [str(e) for e in self.elems]) + "}"
    else:
      return str(self.val)

def tokenize(str):
  return re.findall("(\d+|[^ 0-9])", str)

def parse(tokens):
  if tokens[0] == ")":
    expr, tokens = parse(tokens[1:])
    tokens = tokens[1:]  # Consume the closing parenthesis
  else:
    expr = Expr("", int(tokens[0]), None)
    tokens = tokens[1:]

  if len(tokens) == 0 or tokens[0] == "(":  # End of expression
    return expr, tokens

  op, tokens = tokens[0], tokens[1:]
  right, tokens = parse(tokens)
  return Expr(op, 0, [expr, right]), tokens

# parses "1 + (2 * 3)" into [1, +, [2, *, 3]]
def parse_parens(tokens):
  expr = []

  while len(tokens) > 0 and tokens[0] != "(":  # End of sub-expression
    if tokens[0] == ")":
      elem, tokens = parse_parens(tokens[1:])
    elif tokens[0] in ("+", "*"):
      elem = tokens[0]
    else:
      elem = int(tokens[0])
    tokens = tokens[1:]
    expr.append(elem)

  return expr, tokens

def parse_precedence(groups):
  def splitby(l, op):
    return [list(g) for k, g in groupby(l, lambda x: x == op) if not k]

  if isinstance(groups, list):
    groups = [parse_precedence(g) for g in groups]
    groups = Expr("*", 0, [
      Expr("+", 0, [x[0] for x in splitby(e, "+")])
      for e in splitby(groups, "*")
    ])
    return groups
  elif isinstance(groups, int):
    return Expr("", groups, None)
  else:
    return groups

def eval(expr):
  if expr.op == "*":
    return reduce(lambda x, y: x * y, [eval(e) for e in expr.elems])
  elif expr.op == "+":
    return reduce(lambda x, y: x + y, [eval(e) for e in expr.elems])
  else:
    return expr.val

with open("data/day18a.txt") as f:
  part1, part2 = 0, 0

  for line in f:
    line = line.rstrip()
    tokens = tokenize(line)
    tokens.reverse()
    print(line)

    expr1, _ = parse(tokens)
    print("==>", expr1)
    part1 += eval(expr1)

    groups, _ = parse_parens(tokens)
    expr2 = parse_precedence(groups)
    print("==>", expr2)
    part2 += eval(expr2)

    print("")

  print("part1 =", part1)
  print("part2 =", part2)
