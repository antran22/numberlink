import re
from turtle import width
from puzzle import NumberlinkPuzzle
import pycosat

def solve(puzzle: NumberlinkPuzzle):
    """
    Finds truth value assignments for given cnf_clauses. Returns a list of all literals, which
    are preceded by '-' if they are assigned a False value.
    :param cnf_clauses:
    :return: assignments array. None if the problem is not solvable.
    """
    
    # Initialize model. Keep track of literals in the bool_vars dictionary.
    cnf = puzzle.generate_cnf()
    result = pycosat.solve(cnf)

    if result == "UNSAT":
        print("Cannot solve")
        return
    assignments = []


    result_map = parse_result(result)

    numbers = sorted([key for key in puzzle.var_map if key[0] == 'n' and result_map[puzzle.var_map[key]] > 0])

    output_table = [[" " for i in range(puzzle.width)] for j in range(puzzle.height)]

    for number in numbers:
        x, y, col = number.split('.')[1:]
        
        x = int(x)
        y = int(y)


        v_var = puzzle.vertical_line_var(x, y)
        h_var = puzzle.horizontal_line_var(x, y)
        

        if result_map[v_var] > 0:
            output_table[y][x] = "↓"

        if result_map[h_var] > 0:
            output_table[y][x] = "→"
    
    for i, (x, y) in enumerate(puzzle.number_coordinates):
        output_table[y][x] = i // 2 + 1
        
    for line in output_table:
        for char in line:
            print (char, end=" ")
        print("\n")
        


def parse_result(result):
    return {abs(var): var for var in result}
     