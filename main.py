import argparse
from turtle import pu
from puzzle import NumberlinkPuzzle
from solve import solve
import coordss

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--puzzle", "-p", required=True, type=int)

args = parser.parse_args()

puzzle_index = args.puzzle

puzzle = NumberlinkPuzzle(
    coordss.size[puzzle_index], coordss.size[puzzle_index], coordss.coords[puzzle_index]
)

solve(puzzle)
