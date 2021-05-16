from string import ascii_uppercase
from operator import and_
from functools import reduce


# Splitting function for productions
def splittingFunction(mapper):

    productions = []
    rules = []
    for rule in mapper:
        rules = rule.split(' - ')
        productions.append(rules)
    return productions


# Function to that adds a starting state
def addStartingState(productions, S):

    to_add_S0 = False
    for i in range(len(productions)):
        if productions[i][0] == S:
            to_add_S0 = True
    if to_add_S0:
        productions.append(('S0', S))
        S = 'S0'

    productions = [pair for pair in productions if pair[1] != 'epsilon']

    return productions


# Function to eliminate the terminals
def eliminateTerminals(productions, Vt):

    to_eliminate = set()

    for production in productions:
        to_eliminate.update(set(production[1]).intersection(set(Vt)))

    to_eliminate = list(to_eliminate)
    for production in productions:
        if production[1] in Vt and production[1] in to_eliminate:
                to_eliminate.remove(production[1])

    for element in to_eliminate:
        productions.append((free_uppercase[0], element))
        free_uppercase.pop(0)

    back_mapping = dict()
    for i in range(len(productions)):
        if productions[i][1] in Vt:
            back_mapping[productions[i][1]] = productions[i][0]

    for i in range(len(productions)):
        for key in back_mapping:
            if key in productions[i][1] and len(productions[i][1]) > 1:
                productions[i][1] = productions[i][1].replace(key, back_mapping[key])

    return productions


# Function to eliminate production with more than 2 symbols
def eliminateMoreThan2(productions, free_uppercase):

    # Iterate through all the productions
    for i in productions:

        # Two lists to separate productions by length
        with_2_symbols = []
        with_more_2_symbols = []
        for i in range(len(productions)):
            if len(productions[i][1]) == 2:
                with_2_symbols.append(i)
            elif len(productions[i][1]) > 2:
                with_more_2_symbols.append(i)

        # Check if we have any production of length more than 2
        if len(with_more_2_symbols) == 0:
            break

        for i in with_2_symbols:
            for j in with_more_2_symbols:
                if productions[i][1] in productions[j][1] and i != j:
                    productions[j][1] = productions[j][1].replace(productions[i][1], productions[i][0])

        # Check if there are productions with more than 2 symbols
        if len(with_more_2_symbols) != 0:
            substrings = []

            for i in with_more_2_symbols:
                substrings.append([])
                for j in range(len(productions[i][1]) - 1):
                    substrings[-1].append(productions[i][1][j:j + 2])
            substrings = [set(sub) for sub in substrings]
            common_strings = list(reduce(and_, substrings))

            for common_string in common_strings:
                productions.append([free_uppercase[0], common_string])
                free_uppercase.pop(0)

    return productions


lines = open("variant26CFG.txt", "r").read().split(';\n')

Vt = lines[0].split(' ')
Vn = lines[1].split(' ')
mapper = lines[2].split(', ')

productions = splittingFunction(mapper)

free_uppercase = [letter for letter in ascii_uppercase if letter not in Vn]

new_mappers = eliminateTerminals(addStartingState(productions, 'S'), Vt)
print(eliminateMoreThan2(new_mappers, free_uppercase))

