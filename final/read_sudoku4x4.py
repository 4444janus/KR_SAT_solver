import math as math

def read_sudokus4x4():


    with open('4x4.txt', 'r') as sudo4:
        data4 = sudo4.read()

    sudokus4 = data4.split()
    all_sudokus4 = []

    for sudoku in sudokus4:
        cnf4 = []
        for i in range(0,15):
            if sudoku[i] == ".":
                cnf4 = cnf4
            else:
                l = []
                row = math.floor(i/4)
                row1 = row+1
                l.append(row1)
                col = i - (4*row)+1
                l.append(col)
                l.append(sudoku[i])
                l = int(''.join(map(str, l)))

                cnf4.append(l)
        all_sudokus4.append(cnf4)
    # print(all_sudokus4)
    return all_sudokus4
# read_sudokus4x4()