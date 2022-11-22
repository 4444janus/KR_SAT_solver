import random


def heuristics(heuristic, all_literals, clauses):
    if heuristic == "mom":
        literals = all_literals
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
        choice=max_literal

    elif heuristic == "human":
        num_rows = []
        num_column = []
        list_choice = []
        # print(all_literals)
        for item in range(len(all_literals)):
            literal = [int(x) for x in str(all_literals[item])]
            row_literal, column_literal = literal[0], literal[1]
            num_rows.append(row_literal)
            num_column.append(column_literal)

        min_column = min(set(num_column), key=num_column.count)
        min_row = min(set(num_rows), key=num_rows.count)

        for item in range(len(all_literals)):
            literal = [int(x) for x in str(all_literals[item])]

            # print(literal[1])
            # print(f"minrow:{min_row}")
            # print(f"mincol:{min_column}")
            if literal[0] == min_row and literal[1] == min_column:
                list_choice.append(literal)
            elif literal[0] == min_row:
                list_choice.append(literal)
        # print(list_choice)
        choice_random = random.choice(list_choice)
        choice_str = [str(i) for i in choice_random]
        choice = (int("".join(choice_str)))

    elif heuristic == "first":
        choice = all_literals[0]
    else:
        choice = random.choice(all_literals)

    return choice