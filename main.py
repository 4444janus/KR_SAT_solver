
class SAT:
    def __init__(self, clauses=[], assignment=[], truth_values={}):
        self.clauses = clauses
        self.assignment = assignment
        self.truth_values = truth_values




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
                    negative.append(abs(literal))
        only_positive = [x for x in positive if x not in set(negative)]
        only_negative = [-x for x in negative if x not in set(positive)]

        # twee forloops. loop over literals. checked of literal kleiner is dan 0. if else. om te checken of positief of negatief.
        # if literal is only positive of negative, delete
        for i in only_positive:
            self.truth_values[i] = True
        for i in only_negative:
            self.truth_values[i] = False
        #set truthvalues to true or false

        return only_positive + only_negative

    def unit_clause(self):
        for clause in self.clauses:
            # if
            if len(clause) == 1:
                # is unit clause
                self.truth_values[clause[0]] = True
            else:
                continue
        return self.clauses, self.truth_values

    def check_tautology(self):
        for clause in self.clauses:
            for literal in clause:
                if -literal in clause:
                    print(literal)
                    self.clauses.remove(clause)
        return self.clauses

    def split(self):
        for clause in self.clauses:
            if True:
                return sat
            else:
                self.solve

    def solve(self):
        # if not self.clauses: #TODO
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

                self.pure_literal()
                if self.truth_values no change:

            #not able to simplify:
                    self.split()

# def dpll(clause):
#     if clause == "SAT":
#         return 'sat'
#
#     if  clause == 'tautology':
#         dpll()
#
#     if clause == 'unit clause':
#         dpll(True)
#
#     if clause == 'pure literal':
#         dpll(True)
#
#     if dpll() == True:
#         return 'SAT'
#     else:
#         dpll(False)



if __name__ == '__main__':
    data = 'sudoku-rules-4x4_combined_w_puzzle.txt'
    sat = SAT()
    sat.read_dimacs(data)
    sat.solve()
    # pure_literal(read_dimacs(data))
