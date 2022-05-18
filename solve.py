import re
from time import time
from turtle import width
from puzzle import NumberlinkPuzzle
import pycosat
import pygame

def solve(puzzle: NumberlinkPuzzle):
    """
    Finds truth value assignments for given cnf_clauses. Returns a list of all literals, which
    are preceded by '-' if they are assigned a False value.
    :param cnf_clauses:
    :return: assignments array. None if the problem is not solvable.
    """
    
    # Initialize model. Keep track of literals in the bool_vars dictionary.
    cnf = puzzle.generate_cnf()
    t1 = time()
    result = 0

    n = 0
    while n < 1000:
        n += 1
        print(n)

        result = pycosat.solve(cnf)

        # return if can't solve
        if result == "UNSAT":
            print("Cannot solve")
            return

        if not puzzle.has_circle(cnf, result):
            break

    t2 = time()


    def find_cell(j, i):
        for k in puzzle.number_range():
            if puzzle.number_var(k, i, j) in result:
                return k

    img = []
    for i in range(puzzle.height):
        row = []
        for j in range(puzzle.width):
            row.append(find_cell(i, j))
        img.append(row)

    # get set of variables
    s = set()
    for clause in cnf:
        for num in clause:
            s.add(abs(num))

    print('size:', (puzzle.width, puzzle.height))
    print('numbers:', puzzle.number_count)
    print('time: ', t2-t1, 's', sep='')
    print('variables:', len(s))
    print('clauses:', len(cnf))


    # Show board by pygame
    cell_size = 25
    cell_color = int(255/(puzzle.number_count))
    pygame.init()
    display = pygame.display.set_mode((puzzle.height*cell_size, puzzle.width*cell_size))

    for y in range(puzzle.height):
        for x in range(puzzle.width):
            pygame.draw.rect(display, 
                (cell_color * (img[y][x]-1), cell_color * (img[y][x]-1), cell_color * (img[y][x]-1)), 
                [x*cell_size, y*cell_size, cell_size, cell_size])
    
    for y in range(puzzle.height):
        for x in range(puzzle.width):
            if puzzle.horizontal_line_var(x, y) in result:
                pygame.draw.line(display,
                (255, 0, 0),
                (x*cell_size + cell_size/2, y*cell_size + cell_size/2),
                ((x+1)*cell_size + cell_size/2, y*cell_size + cell_size/2),
                3)
            if puzzle.vertical_line_var(x, y) in result:
                pygame.draw.line(display,
                (255, 0, 0),
                (x*cell_size + cell_size/2, y*cell_size + cell_size/2),
                (x*cell_size + cell_size/2, (y+1)*cell_size + cell_size/2),
                3)

    pygame.display.flip()

    while True:
        continue
     