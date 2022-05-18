from turtle import pu
from puzzle import NumberlinkPuzzle
from solve import solve
import coordss

order = 5

puzzle = NumberlinkPuzzle(coordss.size[order], coordss.size[order], coordss.coords[order])

solve(puzzle)