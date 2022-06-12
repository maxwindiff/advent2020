import re
from typing import NamedTuple

class Expr(NamedTuple):
  op: str
  val: int
  l: 'Expr'
  r: 'Expr'

  def __repr__(self):
    if self.op == "*":
      return f"({self.r} * {self.l})"
    elif self.op ==  "+":
      return f"({self.r} + {self.l})"
    else:
      return str(self.val)

def tokenize(str):
  return re.findall("(\d+|[^ 0-9])", str)

def parse(tokens):
  if tokens[0] == ")":
    expr, tokens = parse(tokens[1:])
    tokens = tokens[1:]  # Consume the closing parenthesis
  else:
    expr = Expr('', int(tokens[0]), None, None)
    tokens = tokens[1:]

  if len(tokens) == 0 or tokens[0] == "(":  # End of expression
    return expr, tokens

  op, tokens = tokens[0], tokens[1:]
  right, tokens = parse(tokens)
  return Expr(op, 0, expr, right), tokens

def eval(expr):
  if expr.op == "*":
    return eval(expr.l) * eval(expr.r)
  elif expr.op == "+":
    return eval(expr.l) + eval(expr.r)
  else:
    return expr.val

with open("data/day18a.txt") as f:
  sum = 0
  for line in f:
    line = line.rstrip()

    tokens = tokenize(line)
    tokens.reverse()
    expr, _ = parse(tokens)
    print(line, "=>", expr)
    print(eval(expr))
    sum += eval(expr)
  print("part1 =", sum)
