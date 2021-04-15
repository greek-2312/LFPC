import re

non_symbols_visited = {}
grammar = dict()
symbols = []
path = []

global grammar, non_symbols_visited


# Splitting the raw text and reading only the values from parenthesizes on a given pattern
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
    
    Vn, Vt, P = [], [], []
    global Vt
    # Read the file
    lines = open("variant26.txt", "r").read().split(';')
    # Splitting lines from the txt file
    Vn = splittingFunction(lines[0])
    Vt = splittingFunction(lines[1])
    P = splittingFunction(lines[2])
    # Mapping the rules in the dictionary
    mappingFunction(P, grammar)


# Function for printing the path of how a word was created
def generatePath(path, input_string):
    for index in range(len(path)):
        if index == 0:
            print(path[index], end=" -> ")
            continue
        print(input_string[0: index] + path[index], end=" -> ")

    print(input_string)


def finiteAutomaton(input_string, start_symbol, non_symbols_visited, sequence, generated_string):

    accepted = False
    global accepted

    # Assume True to the start non-terminal symbol
    non_symbols_visited[start_symbol] = True
    sequence.append(start_symbol)

    # Iterate through the tuples from the dictionary where key == start_symbol
    for tuples in grammar[start_symbol]:

        # Check if the generated string matches the input string
        if generated_string + tuples[0] == input_string and tuples[1] is None:
            accepted = True
            generatePath(sequence, input_string)

        # Check if the length of input string is less than of generated string
        if len(generated_string) > len(input_string) or tuples[1] is None:
            continue

        finiteAutomaton(input_string, tuples[1], non_symbols_visited, sequence, generated_string + tuples[0])

    sequence.pop()
    non_symbols_visited[start_symbol] = False


input_string = str(input('Enter a string: '))
# Call the reading and splitting function
readGrammar()

not_accepted_by_symbols = 0

for symbol in Vt:
    if symbol not in input_string:
        not_accepted_by_symbols += 1

if not_accepted_by_symbols != 0:
    print('There were introduced unavailable symbols.')
else:

    # For keys in grammar dictionary append them to non_symbols_visited
    for key in grammar:
        non_symbols_visited[key] = False

    finiteAutomaton(input_string, "S", non_symbols_visited, path, '')

    if accepted:
        print('Input string was accepted.')
    else:
        print('Input string wasn\'t accepted.')
