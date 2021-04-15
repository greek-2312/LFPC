import networkx as net
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Function to create the NFA dictionary
def construct_nfa_from_file(lines):

    global start_state, final_state, terminal_symbols, states

    start_state = 0
    accepting_states = []
    terminal_symbols = list(lines[0].split(","))
    states = list(lines[1].split(","))
    transition_functions = []
    nfa_transition_dict = {}
    start_state = lines[2]
    final_state = lines[3]

    for index in range(4, len(lines)):
        transition_func_line = lines[index].split(" ")

        starting_state = transition_func_line[0]
        transition_symbol = transition_func_line[1]
        ending_state = transition_func_line[2]

        transition_function = (starting_state, transition_symbol, ending_state)
        transition_functions.append(transition_function)

    for transition in transition_functions:
        starting_state = transition[0]
        transition_symbol = transition[1]
        ending_state = transition[2]

        if (starting_state, transition_symbol) in nfa_transition_dict:
            nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
        else:
            nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]

    return nfa_transition_dict


def dfaTransformer(nfa_mappers, dfa_mappers):

    new_state = ()
    new_state_array = []

    for key in nfa_mappers.copy():

        if len(nfa_mappers[key]) >= 2:

            # Check if the first element from the destination states is a tuple
            if type(nfa_mappers[key][0]) is tuple:

                # Add values from the list that consists of tuple and another element and append them to a list
                for state in nfa_mappers[key][0]:
                    new_state_array.append(state)
                new_state_array.append(nfa_mappers[key][1])

                # Assign the new state appending the elements from previously created list
                new_state = tuple(item for index, item in enumerate(new_state_array)
                                  if item not in new_state_array[:index])
            else:

                # Assign the new state if the element is not a tuple
                new_state = tuple(str(element) for element in nfa_mappers[key] if element not in new_state)

            # Create the new state and append it to the dictionary
            dfa_mappers[key] = [new_state]

        else:

            # Adding another rules which does not met the condition to the DFA dictionary
            dfa_mappers[key] = nfa_mappers[key]

        terminal_symbol = ''

        for state in new_state:

            # Union between states to create a new rule with the new state
            if (state == key[0]) or (state in tuple(key[0])):

                terminal_symbol = key[1]
                for symbol in dfa_mappers[key]:

                    # Create the new key
                    key_new = (new_state, terminal_symbol)

                    # Check if the new key is not in dictionary and create a new rule
                    if key_new not in dfa_mappers:
                        dfa_mappers[(new_state, terminal_symbol)] = [symbol]

                    if key_new in dfa_mappers and symbol not in dfa_mappers[key_new]:
                        dfa_mappers[(new_state, terminal_symbol)].append(symbol)

    new_dfa_mappers = {}

    for key in dfa_mappers.copy():

        # Check the length of value if it is bigger than 2 call the function and create new rules
        if len(dfa_mappers[key]) >= 2:
            dfaTransformer(dfa_mappers, new_dfa_mappers)

        # Else assign DFA dictionary to a value and return it
        else:
            new_dfa_mappers = dfa_mappers

    return new_dfa_mappers


# Function to check and find the states that are final states
def finalState(dfa_mappers):

    final_state_array = []

    for key in dfa_mappers:
        if final_state in dfa_mappers[key]:
            final_state_array.append(dfa_mappers[key]) if dfa_mappers[key] not in final_state_array \
                else final_state_array

    return final_state_array


# Works only for this example of NFA for a more beautiful representation
def transitionTable(dfa_mappers):

    for key in dfa_mappers:
        if key[0] not in states and len(key[0]) <= 3:
            element = ' '.join(element for element in key[0])
            if element not in states:
                states.append(element)

    column_len = len(terminal_symbols)
    row_len = len(states)

    data = np.zeros((row_len, column_len), dtype=int)

    df = pd.DataFrame(data, columns=terminal_symbols)
    plt.axis('off')
    plt.table(cellText=df.values, colLabels=df.columns, rowLabels=states)

    plt.show()


# Works only for this example of NFA for a more beautiful representation
def drawGraph(new_dfa_mappers):

    graph = net.Graph()
    edges_a = []
    edges_b = []
    edges_c = []

    for key in new_dfa_mappers:
        if len(key[0]) <= 3 and len(new_dfa_mappers[key][0]) <= 3 and key[1] == 'a':
            element = (key[0], new_dfa_mappers[key][0])
            edges_a.append(element)
        if len(key[0]) <= 3 and len(new_dfa_mappers[key][0]) <= 3 and key[1] == 'b':
            element = (key[0], new_dfa_mappers[key][0])
            edges_b.append(element)
        if len(key[0]) <= 3 and len(new_dfa_mappers[key][0]) <= 3 and key[1] == 'c':
            element = (key[0], new_dfa_mappers[key][0])
            edges_c.append(element)

    graph.add_edges_from(edges_a, weight=1)
    graph.add_edges_from(edges_b, weight=2)
    graph.add_edges_from(edges_c, weight=3)

    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in graph.edges(data=True)])
    pos = net.spring_layout(graph)
    net.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    net.draw(graph, pos, edge_cmap=plt.cm.Reds, with_labels=True)

    plt.savefig("graph_visualisation1.png")
    plt.show()


# Read the NFA from the text file
lines = open("variant26NFA.txt", "r").read().split('\n')

# Assign NFA to a dictionary
nfa_dictionary = construct_nfa_from_file(lines)
dfa_dictionary = {}

# Create the DFA with new transitions and states
print(dfaTransformer(nfa_dictionary, dfa_dictionary))
print(finalState(dfaTransformer(nfa_dictionary, dfa_dictionary)))

transitionTable(dfaTransformer(nfa_dictionary, dfa_dictionary))

drawGraph(dfaTransformer(nfa_dictionary, dfa_dictionary))

