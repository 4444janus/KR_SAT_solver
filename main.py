import random
import time
from copy import deepcopy



class SAT:
    def __init__(self, clauses=[], assignment=[], truth_values={}, history = {}):
        self.clauses = clauses
        self.assignment = assignment
        self.truth_values = truth_values
        self.history = history





    def read_dimacs(self, data):

        for line in open(data):
            if line.startswith('c'): continue  # comment line in DIMACS is skipped
            if line.startswith('p'):
                nvars, nclauses = line.split()[2:4]
                continue
            clause = [int(x) for x in line[:-2].split()]
            self.clauses.append(clause)
        print(f"clauses: {self.clauses},\nnvars: {nvars}, \nnclauses: {nclauses} ")
        x = set()
        for clause in self.clauses:
            for literal in clause:
                x.add(abs(literal))
        self.truth_values = dict.fromkeys(x, None)
        print(self.truth_values)
        return self.clauses, self.truth_values

    def pure_literal(self):

        positive = []
        negative = []
        for clause in self.clauses:

            for literal in clause:
                if literal > 0:
                    positive.append(literal)
                else:
                    negative.append(literal)
        only_positive = [x for x in positive if x not in set(negative)]
        only_negative = [x for x in negative if -x not in set(positive)]

        # twee forloops. loop over literals. checked of literal kleiner is dan 0. if else. om te checken of positief of negatief.
        # if literal is only positive of negative, delete
        for i in only_negative + only_positive:
            self.update_truthvalues(i)
        # for i in only_positive:
        #     self.truth_values[i] = True
        # for i in only_negative:
        #     self.truth_values[i] = False
        #set truthvalues to true or false

        # return only_positive + only_negative

    def unit_clause(self):
        unit = True
        while unit:
            any_units = 0
            for clause in [*self.clauses]:
                # if
                if len(clause) == 1:
                    # is unit clause
                    self.update_truthvalues(clause[0])
                    # self.truth_values[clause[0]] = True
                    self.clauses.remove(clause)
                    any_units += 1

            if any_units == 0:
                unit = False

        # return self.clauses, self.truth_values

    def check_tautology(self):
        for clause in self.clauses:
            # print(clause)
            for literal in clause:
                if -literal in clause:
                    print(literal)
                    self.clauses.remove(clause)
        return self.clauses

    def dpll(self, clauses, truthvalues):
        stuck = True
        if [] in self.clauses:
            return False
        elif self.clauses == len(0):
            return True
        else:
            while not stuck:
                self.unit_clause()

                self.pure_literal()
            if [] in self.clauses:
                return False
            elif self.clauses == len(0):
                return True

            deepcopy_clauses = deepcopy(self.clauses)
            deepcopy_truth_values = deepcopy(self.truth_values)

            all_literals = []
            for literal in self.truth_values:
                if self.truth_values[literal] is None:
                    all_literals.append(literal)
            heuristic = False
            #choose heuristic:
            if heuristic == 1:
                # Maximum Occurence of Minimum size clause (MOM)
                # determine minimum size and select all clauses of this size
                length_of_minimum_clauses = len(min(clauses, key=len))
                minimum_clauses = [x for x in clauses if len(x) == length_of_minimum_clauses]

                # transform nested list in list
                def flat(lis):
                    flatList = []
                    # Iterate with outer list
                    for element in lis:
                        if type(element) is list:
                            # Check if type is list than iterate through the sublist
                            for item in element:
                                flatList.append(item)
                        else:
                            flatList.append(element)
                    return flatList


                flat_clause = flat(minimum_clauses)


                max_occurence = 0
                max_literal = []
                k = 2
                # check for all literals which occurs the most time.
                for literal in literals:
                    occ_lit = (flat_clause.count(literal))
                    occ_lit_prime = (flat_clause.count(-literal))
                    occurence = (occ_lit + occ_lit_prime) * 2 ** k + (occ_lit * occ_lit_prime)
                    if occurence > max_occurence:
                        max_occurence = occurence
                        max_literal = literal
                    else:
                        max_occurence = max_occurence
                        max_literal = max_literal

                # pick the literal with maximum occurence
                choice = max_literal

            elif heuristic == 2:
                pass #TODO

            else:
                choice = random.choice(all_literals)

            # if choice in self.history:
                # if self.history[choice] == True:
                    # Try False
                # else:
            #         Try False
            self.update_truthvalues(choice)
            # self.truth_values[choice] = True
            self.update_clauses()

            result = self.dpll()
            if result:
                return self.truth_values, self.clauses, result

            # else not solved, backtrack

            self.update_truthvalues(-choice)

            return self.dpll()




        # check if able to simplify with dpll. If solve not possible (dpll gives result false) backtrack




        # simplify

        for clause in self.clauses:
            if True:
                return sat
            else:
                self.solve

    def solve(self):
        self.check_tautology()  # check only once at the beginning
        able_to_simplify = True

        self.dpll()

        # simplify:
        self.dpll()

        self.split()




        if [] in self.clauses:
            print('UNSAT')

        elif not self.clauses:
            print("SAT")
        else:
            self.check_tautology() # check only once at the beginning
            able_to_simplify = True
            while able_to_simplify:
                # simplify:
                self.unit_clause()

            # for i in range(2):
            #
            #     self.pure_literal()
            #     if self.truth_values no change:
            #
            # #not able to simplify:
            #         self.split()
    def update_truthvalues(self, literal):
        if literal > 0:
            self.truthvalues[literal] = True
        else:
            self.truthvalues[abs(literal)] = False


    def update_clauses(self):
        changed = False
        clause_not_removed = True
        for clause in [*self.clauses]:
            abs_literal = [abs(literal) for literal in clause]
            for literal in abs_literal:
                if self.truth_values[literal] is True:
                    if literal in clause & clause_not_removed:
                        self.clauses.remove(clause)
                        clause_not_removed = False
                        changed = True
                    elif -literal in clause & clause_not_removed:
                        self.clauses[clause].remove(-literal)
                        changed = True
                elif self.truth_values[literal] is False & clause_not_removed:
                    if -literal in clause & clause_not_removed:
                        self.clauses.remove(clause)
                        clause_not_removed = False
                        changed = True
                    elif literal in clause & clause_not_removed:
                        self.clauses[clause].remove(literal)
                        changed = True
        return changed








def dpll(clause):
    if clause == "SAT":
        return 'sat'

    if  clause == 'tautology':
        dpll()

    if clause == 'unit clause':
        dpll(True)

    if clause == 'pure literal':
        dpll(True)

    if dpll() == True:
        return 'SAT'
    else:
        dpll(False)







if __name__ == '__main__':
    data = 'sudoku-rules-4x4_combined_w_puzzle.txt'
    sat = SAT()
    sat.read_dimacs(data)
    sat.solve()
    # pure_literal(read_dimacs(data))
