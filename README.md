# Laboratory Work Task No. 1 Regular Grammar to Finite Automato

Using Finite Automaton (FA) check if some input string is accepted by FA (meaning you could generate that string by traversing FA).

Accepted string:

<img src="/venv/dfa_accepted.PNG"/>

String was not accepted:

<img src="/venv/dfa_notaccept.PNG"/>

The task is implemented in 'DFA.py' file.

# Laboratory Work Task No. 2 NFA to DFA conversion

Write program which converts nondeterministic finite automato (NFA) to deterministic finite automato (DFA).

### Visualisation of the DFA:

<img src="/venv/dfa_capture.PNG">

Where 1, 2 and 3 are terminal symbols. I wasn't able to implement the self-loops, because it was impossible for me to install pygraphviz package. But this visualisation
is possible for every grammar included in the text file.

### New transitions and all the rules obtained from transforming an NFA to DFA are stored in a dictionary.

<img src="/venv/dfa_console.PNG">

The task is implemented in 'NFAtoDFA.py' file.

# Laboratory Work Task No. 3 CFG to CNF conversion

Tasks:

  1.Eliminate ε productions.
 
  2.Eliminate any renaming.
  
  3.Eliminate inaccessible symbols.
  
  4. Eliminate the non productive symbols.
  
  5. Obtain the Chomsky Normal Form

Variant No. 26:

<img src="/venv/cfg.PNG">

The output of the program:

<img src="/venv/image_2021-05-17_020155.png">
