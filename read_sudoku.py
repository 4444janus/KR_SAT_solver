import numpy as np
import math as math
import collections


def read_sudokus():

    with open('1000 sudokus.txt', 'r') as sudo:
        data = sudo.read()

    sudokus = data.split()
    # print(len(sudokus))
    all_sudokus = []
    for sudoku in sudokus:

        cnf = []
        for i in range(0,80):
            if sudoku[i] == ".":
                cnf = cnf
            else:
                l = []
                row = math.floor(i/9)
                row1 = row+1
                l.append(row1)
                col = i - (9*row)+1
                l.append(col)
                l.append(sudoku[i])
                l = int(''.join(map(str, l)))

                cnf.append(l)
        all_sudokus.append(cnf)
    # print(all_sudokus)
    print(len(all_sudokus))
    return all_sudokus
# read_sudokus()