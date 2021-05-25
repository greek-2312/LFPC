import re
from collections import defaultdict


# Splitting function
def splittingFunction(raw_text):
    raw_text = re.findall('\{(.*?)\}', raw_text)
    symbols = raw_text[0].split(', ')
    return symbols


# Function for mapping the rules with non-terminal symbols
def mappingFunction(P, grammar):
    for grammar_rule in P:
        grammar_element = grammar_rule.split(" - ")
        next_symbol = grammar_element[1][1] if len(grammar_element[1]) == 2 else None

        if grammar_element[0] not in grammar:
            grammar[grammar_element[0]] = []

        grammar[grammar_element[0]].append((grammar_element[1][0], next_symbol))
    return grammar


# Function for reading the txt file
def readGrammar():

    lines = open("variant26.txt", "r").read().split(';')

    Vn = splittingFunction(lines[0])
    Vt = splittingFunction(lines[1])
    P = splittingFunction(lines[2])

    grammar = dict()
    mappingFunction(P, grammar)
    return Vn, Vt, grammar


def firstOf(non_terminal, grammar, vt):

    first = []
    non_terminal_productions = grammar[non_terminal]

    for production in non_terminal_productions:
        if production[0] in vt or production[0] == 'e':
            first.append(production[0])
            continue
        nonTerminalFirst = production[0]

        first.extend(firstOf(nonTerminalFirst, grammar, vt))
    return first


def followOf(non_terminal, grammar, vt):
    follow = []

    rhs_searched_non_terminal_productions = getProductionsRHSWithSearchedNonTerminal(non_terminal, grammar)

    if non_terminal == 'S':
        follow.append("$")

    # Non terminal left
    for non_terminal_lhs in rhs_searched_non_terminal_productions:
        for production in rhs_searched_non_terminal_productions[non_terminal_lhs]:
            index_of_searched_non_terminal = production.index(non_terminal)

            # Right recursion
            if len(production) == index_of_searched_non_terminal + 1 and non_terminal_lhs == non_terminal:
                continue

            # Right recursion if empty string
            if len(production) == index_of_searched_non_terminal + 1 or production[index_of_searched_non_terminal + 1] == "e":
                follow.extend(followOf(non_terminal_lhs, grammar, vt))
                continue

            if production[index_of_searched_non_terminal + 1] in vt:
                follow.append(production[index_of_searched_non_terminal + 1])
                continue

            follow.extend(firstOf(production[-1], grammar, vt))

    return follow


# Get productions where on the right hand side includes the given searchedNonTerminal
def getProductionsRHSWithSearchedNonTerminal(searched_non_terminal, grammar):
    productions = {}

    for nonTerminal in grammar:
        for production_result in grammar[nonTerminal]:
            if searched_non_terminal in production_result:
                if nonTerminal not in productions:
                    productions[nonTerminal] = []

                productions[nonTerminal].append(production_result)
    return productions


# Parsing table
def getParsingTable(grammar, vt, vn):
    parsing_table = [[0 for _ in range(len(vt) + 2)] for _ in range(len(vn) + 1)]

    column_indexes = {}
    for i in range(len(vt)):
        column_indexes[vt[i]] = i + 1
        parsing_table[0][i + 1] = vt[i]

    parsing_table[0][len(vt) + 1] = "$"

    for i in range(len(vn)):
        parsing_table[i + 1][0] = vn[i]
        first_of_non_terminal_list = firstOf(vn[i], grammar, vt)
        for first in first_of_non_terminal_list:
            if first == "e":
                followOfNonTerminalList = followOf(vn[i], grammar, vt)
                for follow in followOfNonTerminalList:
                    parsing_table[i + 1][column_indexes[follow]] = "e"
                continue
            if len(grammar[vn[i]]) == 1:
                parsing_table[i + 1][column_indexes[first]] = grammar[vn[i]][0]
                continue

            for rule in grammar[vn[i]]:
                if rule[0] == "e":
                    continue
                if rule[0] in vt:
                    if rule[0] == first:
                        parsing_table[i + 1][column_indexes[first]] = rule
                    continue
                first_of_rule = firstOf(rule[0], grammar, vt)
                if first_of_rule[0] == column_indexes[first]:
                    parsing_table[i + 1][column_indexes[first]] = rule
                    continue
    return parsing_table


def getTableTerminalIndexes(parsing_table):
    terminalIndexes = {}
    for i in range(1, len(parsing_table[0])):
        terminalIndexes[parsing_table[0][i]] = i
    return terminalIndexes


def getTableNonTerminalIndexes(parsing_table):
    nonTerminalIndexes = {}
    for i in range(1, len(parsing_table)):
        nonTerminalIndexes[parsing_table[i][0]] = i
    return nonTerminalIndexes


def parseString(input_string, parsing_table, vn):
    input_string_copy = input_string + "$"
    current_input_symbol = input_string_copy[0]
    stack = ['S', '$']

    non_terminal_indexes = getTableNonTerminalIndexes(parsing_table)
    terminalIndexes = getTableTerminalIndexes(parsing_table)

    # While there are elements in stack
    while len(stack):
        current_stack_symbol = stack[0]

        # There are no more elements in stack
        if current_stack_symbol == current_input_symbol and current_stack_symbol == "$":
            return
        if current_stack_symbol == current_input_symbol:
            input_string_copy = input_string_copy[1: len(input_string_copy)]
            stack.pop(0)

            current_input_symbol = input_string_copy[0]
            continue
        if current_stack_symbol in vn:
            replacement_production = parsing_table[non_terminal_indexes[current_stack_symbol]][
                terminalIndexes[current_input_symbol]]
            stack.pop(0)

            for symbol in reversed(replacement_production):
                if symbol == 'e':
                    continue
                stack.insert(0, symbol)
            print(current_stack_symbol + ' -> ' + "".join(replacement_production))


Vn, Vt, grammar = readGrammar()
parsingTable = getParsingTable(grammar, Vt, Vn)
parseString("bacaebdbaca", parsingTable, Vn)
