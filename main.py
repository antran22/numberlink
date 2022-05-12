from turtle import pu
from puzzle import NumberlinkPuzzle
from solve import solve


coords = [
    (2, 5),
    (4, 2),
    (0, 6),
    (4, 1),
    (1, 1),
    (3, 2),
    (3, 0),
    (4, 6),
    (3, 3),
    (5, 1)
]

puzzle = NumberlinkPuzzle(7, 7, coords)

solve(puzzle)