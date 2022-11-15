
class SAT:
    def __init__(self, clauses=[], assignment=[], truth_values={}):
        self.clauses = clauses
        self.assignment = assignment
        self.truth_values = truth_values
8
    def read_dimacs(self, data):

        for line in open(data):
            if line.startswith('c'): continue  # comment line in DIMACS is skipped
            if line.startswith('p'):
                nvars, nclauses = line.split()[2:4]
                continue
            clause = [int(x) for x in line[:-2].split()]
            self.clauses.append(clause)
        # print(f"clauses: {self.clauses},\nnvars: {nvars}, \nnclauses: {nclauses} ")
        x = set()

        for clause in self.clauses:
            for literal in clause:
                x.add(abs(literal))
                
        self.truth_values = dict.fromkeys(x, None)
        # print(self.truth_values)
        self.clauses_dup = self.clauses
        # print(self.clauses)
        return self.clauses, self.truth_values, self.clauses_dup

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

        print(self.truth_values)
        
        return self.clauses, self.truth_values

    def check_tautology(self):
        for clause in self.clauses:
            for literal in clause:
                if -literal in clause:
                    # print(f'this will be removed literal {literal}')
                    self.clauses.remove(clause)
        return self.clauses

    def split(self, num):

        """
        The input number will be put on True in the self.clauses list. Numbers in the same list as the
        input nummber are set to False. The dict is updated accordingly.
        """

        # print("this is the beginning of the split")
        # print(self.truth_values)
        # print(self.clauses)

        # create empty set for
        set_false = set()

        # check each clause
        for clause in self.clauses:
            # print(clause)

            # check each literal in the clause
            for literal in range(len(clause)):

                # set a certain literal to True in each clause and in the dictonary
                if clause[literal] == num or clause[literal] == -num:
                    clause[literal] = True
                    self.truth_values[num] = True

            # add values that must be false to a set
            if True in clause:
                # print(clause)
                set_false.update(clause)

        set_false.remove(True)

        # set each value that must be false to false
        for clause in self.clauses:
            # print(clause)

            for literal in range(len(clause)):

                # print(literal)

                if clause[literal] in set_false:
                    # print(clause[literal])
                    self.truth_values[clause[literal]] = False
                    clause[literal] = False

            # print(clause)

        # print(set_false)

        # print('this is the final split')
        # print(self.truth_values)
        # print(self.clauses)
        # print(set_false)
        return self.clauses, self.truth_values


    def solve(self):

        """
        Het leek me logisch om over de keys van de dict te lopen en daarmee de split functie
        te kunnen gebruiken, maar ik snapte niet wat dan op een hoger niveau moest, de while loop of for loop
        """
        # self.check_tautology()  # check only once at the beginning

        keys = list(self.truth_values.keys()) # ik wil deze sorteren maar idk hoe want .sort() werkt niet
        # print(keys)
        able_to_simplify = True
        count = 0

        while able_to_simplify:
            # simplify:
            for item in keys:
                self.pure_literal()
                self.unit_clause()
                self.solve(item)


            count += 1
            if count == 3:
                able_to_simplify = False

    def solve2(self):

        """Dit was de oude solve functie maar wilde deze nog niet weg doen"""
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
    sat.split(111)
    # sat.check_tautology()
    # sat.unit_clause()
    # pure_literal(read_dimacs(data))
    # sat.solve()