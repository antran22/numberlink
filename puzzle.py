from dataclasses import dataclass
from itertools import product, combinations
from math import comb
from typing import Iterable, List, Optional, Tuple

Coordinate = Tuple[int, int]


class NumberlinkPuzzle:
    """
    A Numberlink puzzle class that takes the puzzle width, height, and the locations of the colors
    (numbers) at initialization. Contains a conjunctive normal form (CNF) generator and solver
    methods.
    """

    def __init__(self, width: int, height: int, number_coordinates: List[Coordinate]):
        self.width = width
        self.height = height
        self.number_count = len(number_coordinates) // 2
        self.number_coordinates = number_coordinates
        self.area = width * height
        self.generate_var_map()
        self.graph = self.generate_graph()

    def generate_cnf(self):
        cnf_clauses = []
        for y in range(self.height):
            for x in range(self.width):
                cnf_clauses.extend(self.cnf_for_cell(x, y))

        # Add respective numbers to given color locations.
        for i in self.number_range():
            coord_1, coord_2 = self.coordinate_for_number(i)

            cnf_clauses.append([self.number_var(i, coord_1[0], coord_1[1])])

            cnf_clauses.append([self.number_var(i, coord_2[0], coord_2[1])])

        return cnf_clauses

    def cnf_for_cell(self, x: int, y: int):
        cnf_clauses = []
        lines: List[int] = []

        # All vertical and horizontal lines attached to current cell.
        if x != self.width - 1:
            lines.append(self.horizontal_line_var(x, y))
        if y != self.height - 1:
            lines.append(self.vertical_line_var(x, y))
        if x != 0:
            lines.append(self.horizontal_line_var(x - 1, y))
        if y != 0:
            lines.append(self.vertical_line_var(x, y - 1))

        # Every color cell has only 1 line going in/out, every non-color cell
        # has 2 lines going in/out. Denoting corresponding logic in CNF.
        # (1 or 2 True out of 2, 3 or 4 literals).
        if (x, y) in self.number_coordinates:
            for combination in combinations(lines, 2):
                cnf_clauses.append(negative_cnf(combination))
            cnf_clauses.append(positive_cnf(lines))
        else:
            # 2 true out of 2 lines.
            if len(lines) == 2:
                for l in lines:
                    cnf_clauses.append([l])
            # 2 true out of 3 lines.
            elif len(lines) == 3:
                for combination in combinations(lines, 2):
                    cnf_clauses.append(positive_cnf(combination))
                cnf_clauses.append(negative_cnf(lines))
            # 2 true out of 4 lines.
            else:
                for combination in combinations(lines, 3):
                    cnf_clauses.append(positive_cnf(combination))
                    cnf_clauses.append(negative_cnf(combination))

        # Number variables for current cell. Only 1 is True.
        number_vars = [self.number_var(number, x, y) for number in self.number_range()]
        for combination in combinations(number_vars, 2):
            cnf_clauses.append(negative_cnf(combination))
        cnf_clauses.append(number_vars)

        # Vertical/horizontal line implies color shared with adjacent cell.
        if self.horizontal_line_var(x, y) in lines:
            cur_numbers = [
                (self.number_var(number, x, y), self.number_var(number, x + 1, y))
                for number in self.number_range()
            ]
            for double in product(*cur_numbers):
                cnf_clauses.append([-self.horizontal_line_var(x, y), *double])

        if self.vertical_line_var(x, y) in lines:
            cur_numbers = [
                (self.number_var(number, x, y), self.number_var(number, x, y + 1))
                for number in self.number_range()
            ]

            for double in product(*cur_numbers):
                cnf_clauses.append([-self.vertical_line_var(x, y), *double])

        return cnf_clauses

    # check circle and add cnf
    def has_circle(self, result):
        visited = []

        lined = set()
        coorded = set()
        queue = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in visited:
                    lined.clear()
                    coorded.clear()
                    queue.clear()
                    coorded.add((x, y))
                    queue.append((x, y))
                    last_var = 0
                    while len(queue) > 0:
                        xx, yy = queue.pop()
                        for var, coord in self.graph[yy][xx]:
                            if var in result and var != last_var:
                                if var in lined:
                                    return False
                                lined.add(var)
                                coorded.add(coord)
                                queue.append(coord)
                                last_var = var
                                break
                    visited.extend(coorded)
        return True

    def generate_graph(self):
        graph = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = []
                if x != self.width - 1:
                    cell.append([self.horizontal_line_var(x, y), (x + 1, y)])
                if y != self.height - 1:
                    cell.append([self.vertical_line_var(x, y), (x, y + 1)])
                if x != 0:
                    cell.append([self.horizontal_line_var(x - 1, y), (x - 1, y)])
                if y != 0:
                    cell.append([self.vertical_line_var(x, y - 1), (x, y - 1)])
                row.append(cell)
            graph.append(row)
        return graph

    def coordinate_for_number(self, number: int) -> Tuple[Coordinate, Coordinate]:
        return (
            self.number_coordinates[number * 2 - 2],
            self.number_coordinates[number * 2 - 1],
        )

    def number_at_coordinate(self, x: int, y: int) -> Optional[int]:
        if (x, y) not in self.number_coordinates:
            return None
        idx = self.number_coordinates.index((x, y))
        return idx // 2 + 1

    def horizontal_line_var(self, x: int, y: int) -> int:
        return self.var_map[f"h.{x}.{y}"]

    def vertical_line_var(self, x: int, y: int) -> int:
        return self.var_map[f"v.{x}.{y}"]

    def number_var(self, number: int, x: int, y: int) -> int:
        return self.var_map[f"n.{x}.{y}.{number}"]

    def number_range(self):
        return range(1, self.number_count + 1)

    def generate_var_map(self):
        self.var_map = {}
        self.var_array = [None]
        for x in range(self.width):
            for y in range(self.height):
                v = f"v.{x}.{y}"
                self.var_map[v] = len(self.var_array)
                self.var_array.append(v)

                h = f"h.{x}.{y}"
                self.var_map[h] = len(self.var_array)
                self.var_array.append(h)

                for number in self.number_range():
                    n = f"n.{x}.{y}.{number}"
                    self.var_map[n] = len(self.var_array)
                    self.var_array.append(n)


def positive_cnf(elements: Iterable[int]) -> List[int]:
    return list(elements)


def negative_cnf(elements: Iterable[int]) -> List[int]:
    return [-e for e in elements]
