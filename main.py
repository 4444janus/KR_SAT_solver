import time
from copy import deepcopy
import pandas as pd
from read_sudoku import read_sudokus
from pathlib import Path
from heuristics import heuristics
class SAT:
    def __init__(self, amount_of_splits=0, amount_of_backtracks=0, amount_of_simplify=0, solution=[]):
        # self.clauses = clauses
        # self.assignment = assignment
        # self.truth_values = truth_values

        self.amount_of_splits = amount_of_splits
        self.amount_of_backtracks = amount_of_backtracks
        self.amount_of_simplify = amount_of_simplify
        self.solution = solution

    def read_dimacs(self, data):
        clauses = []

        for line in open(data):
            if line.startswith('c'): continue  # comment line in DIMACS is skipped
            if line.startswith('p'):
                nvars, nclauses = line.split()[2:4]
                continue
            clause = [int(x) for x in line[:-2].split()]
            clauses.append(clause)
        # print(f"clauses: {clauses},\nnvars: {nvars}, \nnclauses: {nclauses} ")
        x = set()
        for clause in clauses:
            for literal in clause:
                x.add(abs(literal))
        truth_values = dict.fromkeys(x, None)

        return clauses, truth_values

    def pure_literal(self, clauses, truth_values):

        positive = []
        negative = []
        for clause in clauses:

            for literal in clause:
                if literal > 0:
                    positive.append(literal)
                else:
                    negative.append(literal)
        only_positive = [x for x in positive if -x not in set(negative)]
        only_negative = [x for x in negative if -x not in set(positive)]

        # twee forloops. loop over literals. checked of literal kleiner is dan 0. if else. om te checken of positief of negatief.
        # if literal is only positive of negative, delete
        for i in only_positive + only_negative:

            self.update_truthvalues(i, truth_values)


    def unit_clause(self, clauses, truth_values):
        unit = True
        changed = False
        while unit:
            any_units = 0
            for clause in [*clauses]:
                if len(clause) == 1:
                    # is unit clause
                    self.update_truthvalues(clause[0], truth_values)

                    clauses_new, truth_values, changed = self.update_clauses(clauses, truth_values)
                    any_units += 1

            if any_units == 0:
                unit = False
        return clauses, truth_values, changed


    def check_tautology(self, clauses):
        for clause in clauses:
            for literal in clause:
                if -literal in clause:
                    clauses.remove(clause)
        return clauses

    def dpll(self, clauses, truth_values):

        if [] in clauses:

            return clauses, truth_values, False
        elif not clauses:

            return clauses, truth_values, True
        else:
            able_to_simplify = True
            while able_to_simplify:

                self.amount_of_simplify += 1

                changed = self.unit_clause(clauses, truth_values)

                self.pure_literal(clauses, truth_values)
                clauses, truth_values, able_to_simplify = self.update_clauses(clauses, truth_values)
                if changed is True:
                    able_to_simplify = True

            #check if already satisfiable or not
            if [] in clauses:

                return truth_values, clauses, False

            elif not clauses:

                return truth_values, clauses, True


            #make copy for backtracking
            clauses_before_splitting = deepcopy(clauses)
            truth_values_before_splitting = deepcopy(truth_values)

            all_literals = []
            for literal in truth_values:
                if truth_values[literal] is None:
                    all_literals.append(literal)


            #choose heuristic:
            print(f"all_literals: {all_literals}")
            choice = heuristics(heuristic, all_literals, clauses)
            print(f"choice: {choice}")
            print(f"all_literals: {all_literals}")

            self.amount_of_splits += 1

            self.update_truthvalues(choice, truth_values)
            # self.truth_values[choice] = True
            clauses_before_splitting, truth_values_before_splitting, changed = self.update_clauses(clauses_before_splitting, truth_values_before_splitting)

            truth_values, clauses, result = self.dpll(clauses, truth_values)
            if result:

                return truth_values, clauses, result

            # else not solved, backtrack

            self.update_truthvalues(-choice, truth_values_before_splitting)


            self.amount_of_backtracks += 1
            truth_values, clauses, result = self.dpll(clauses_before_splitting, truth_values_before_splitting)

            return truth_values, clauses, result



    def solve(self, clauses, truth_values):

        self.check_tautology(clauses)  # check only once at the beginning
        able_to_simplify = True

        truth_values, clauses, result = self.dpll(clauses, truth_values)

        if [] in clauses:

            for k, v in truth_values.items():
                if v is True:
                    print(k, v)
            print("unsat")
            print(f"Amount of backtracks: {self.amount_of_backtracks}")
            print(f"Amount of simplify: {self.amount_of_simplify}")

            return False

        if not clauses:
            sol = []
            for k, v in truth_values.items():
                if v is True:
                    sol.append(k)
                    # self.solution.append(k)
                #     # print(k, v)
            self.solution = sol
            print("sat")
            print(f"Amount of backtracks: {self.amount_of_backtracks}")
            print(f"Amount of simplify: {self.amount_of_simplify}")

            return True
        else:
            self.dpll(clauses, truth_values)

            able_to_simplify = True

    def update_truthvalues(self, literal, truth_values):
        if literal > 0:
            truth_values[literal] = True
        else:
            truth_values[abs(literal)] = False


    def update_clauses(self, clauses, truth_values):
        changed = False

        for clause in [*clauses]:
            clause_not_removed = True

            # Remove clauses that contain a positive or negative literal that's True.
            # Remove the literals that are True from all clauses.

            abs_literal = [abs(literal) for literal in clause]
            for literal in abs_literal:
                if truth_values[literal] is True:
                    if (literal in clause) & clause_not_removed:
                        clauses.remove(clause)
                        clause_not_removed = False
                        changed = True

                    elif (-literal in clause) & clause_not_removed:
                        # print(f"clauses: {clauses}, clause: {clause}, Literal: {literal}")
                        clause.remove(-literal)
                        changed = True

                elif truth_values[literal] is False & clause_not_removed:
                    if (-literal in clause) & clause_not_removed:
                        clauses.remove(clause)
                        clause_not_removed = False
                        changed = True
                    elif (literal in clause) & clause_not_removed:
                        clause.remove(literal)
                        changed = True
        return clauses, truth_values, changed


if __name__ == '__main__':
    # data = 'sudoku-rules-4x4_combined_w_puzzle.txt'
    data9x9 = "sudoku1.txt"
    puzzle2 = "sudoku2.txt"
    global heuristic
    # heuristic = 2
    # sat = SAT()
    # start_time = time.time()
    # clauses, truth_values = sat.read_dimacs(puzzle2)
    # sat.solve(clauses, truth_values)
    # runtime = time.time() - start_time
    # number_of_splits = sat.amount_of_updates
    # number_of_backtracks = sat.amount_of_backtracks
    # number_of_simplifications = sat.amount_of_simplify
    # TODO create for loop over all sudokus and add results to dataframe

    type = "9x9"
    data = []
    # assign directory
    directory = "1000sudokus"

    # iterate over files in
    # that directory
    files = Path(directory).glob('*')
    for file in files:
        heuristic = 2
        sat = SAT()
        start_time = time.time()
        clauses, truth_values = sat.read_dimacs(file)
        sat.solve(clauses, truth_values)
        runtime = time.time() - start_time
        number_of_splits = sat.amount_of_splits
        number_of_backtracks = sat.amount_of_backtracks
        number_of_simplifications = sat.amount_of_simplify
        solution = sat.solution
        # print(f"solution: {solution}")
        print("--- %s seconds ---" % runtime)
        data.append([type, heuristic, runtime, number_of_splits, number_of_backtracks, number_of_simplifications, solution])
        break
    # print(sat.tru)
    print("--- %s seconds ---" % runtime)
    print("number of splits: %i" % number_of_splits)
    print("number of backtracks: %i" % number_of_backtracks)
    print("number of simplifications: %i" % number_of_simplifications)

    # for puzzle in sudokus:
    #     sat = SAT()
    #     sat.solve()


    print(data)


    df = pd.DataFrame(data, columns=["type","heuristic", "runtime", "number of splits", "number of backtracks", "number of simplifications", "solution"])
    df.head()
    df.to_csv("results.csv")
    #write out csv file from dataframe
