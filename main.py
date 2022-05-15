from turtle import pu
from puzzle import NumberlinkPuzzle
from solve import solve


# coords = [
#     (2, 5), (4, 2),
#     (0, 6), (4, 1),
#     (1, 1), (3, 2),
#     (3, 0), (4, 6),
#     (3, 3), (5, 1)
# ]

# puzzle = NumberlinkPuzzle(7, 7, coords)

coords = [
    (0, 5), (4, 4),
    (2, 2), (5, 5),
    (2, 3), (2, 7),
    (5, 4), (4, 10),
    (5, 3), (8, 1),
    (7, 7), (5, 9),
    (6, 5), (9, 6),
    (6, 6), (6, 9),
    (10, 1), (10, 12),
    (10, 2), (14, 12)
]

puzzle = NumberlinkPuzzle(15, 15, coords)

solve(puzzle)