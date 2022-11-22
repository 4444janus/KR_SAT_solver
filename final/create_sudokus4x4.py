from read_sudoku4x4 import read_sudokus4x4
from pathlib import Path
import os

def create_sudoku():
    rules4 = open("sudoku-rules-4x4.txt", "r")
    rules = rules4.read()
    # print(rules)
    all_sudokus = read_sudokus4x4()
    count = 0
    for sudoku in all_sudokus:
        file = open(f"4x4/sudoku{count}.txt", "w")
        for literals in sudoku:
            file.write(f"{literals} 0\n")
        for rule in rules:
            file.write(str(rule))

        file.close()
        count += 1







    # for rule in rules9:
    #     print(rule)
    #     file.write(f"{rule}")

    # file.close
    # with open("1000sudokus/demofile3.txt", "a") as myfile:
    #     myfile.write(rules9)

create_sudoku()