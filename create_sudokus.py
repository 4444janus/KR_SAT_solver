from read_sudoku import read_sudokus
from pathlib import Path
import os

dir_path = Path("/1000sudokus")
file_name = 'mydocument.txt'
file_path = dir_path.joinpath(file_name)
print(file_path)
# check if directory exists
if dir_path.is_dir():

    # check if file already exists
    if file_path.is_file():
        print('File already exists.')
    else:
        with open (dir_path.joinpath(file_name),'w') as f:
            f.write("This text is written with Python.")
            print('File was created.')
else:
    print('Directory doesn\'t exist, please create the directory first.')
def create_sudoku():
    rules9 = open("sudoku-rules-9x9.txt", "r")
    rules = rules9.read()
    print(rules)
    all_sudokus = read_sudokus()
    count = 0
    for sudoku in all_sudokus:
        file = open(f"1000sudokus/sudoku{count}.txt", "w")
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