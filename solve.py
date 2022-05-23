import re
from time import time
from puzzle import NumberlinkPuzzle
import pycosat
import pygame

def solve(puzzle: NumberlinkPuzzle):

    cnf = puzzle.generate_cnf()
    result = 0
    start_time = time()
    for result in pycosat.itersolve(cnf):
        if result == "UNSAT":
            print("Cannot solve")
            return

        if not puzzle.has_circle(result):
            break
    end_time = time()

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

    print('puzzle size:', (puzzle.width, puzzle.height))
    print('numbers:', puzzle.number_count)
    print('time: ', end_time - start_time, 's', sep='')
    print('number of variables:', len(puzzle.var_map))
    print('number of clauses:', len(cnf))


    # Show board by pygame
    cell_size = 25
    cell_color = int(255/(puzzle.number_count))
    pygame.init()
    display = pygame.display.set_mode((puzzle.height*cell_size, puzzle.width*cell_size))
    font = pygame.font.SysFont('Comic Sans MS', 20)

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

            possible_number = puzzle.number_at_coordinate(x, y)
            if possible_number is not None:
               text_surface = font.render(f"{possible_number}", False, (0, 255, 0)) 
               display.blit(text_surface, (x*cell_size + cell_size/2 - 5, y*cell_size + cell_size/2 - 10))
            

    pygame.display.flip()

    while True:
        continue
     