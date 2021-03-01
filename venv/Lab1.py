# Two empty lists for terminal and non-terminal symbols
vt = []
vn = []
# List for storing the set of rules
grammarList = []
# Dictionary for creating the dependencies between NT and T symbols
grammar = dict()
# Setting the boolean value of False as default
isAnswerFound = False

def parseGrammar():
    global vt, vn, grammar
    # Reading the text file
    file = open("variant26.txt", "r")
    fileContent = file.read()
    # Storing in the list vn the terminal symbols
    vn = (fileContent[fileContent.index("VN") + 4:fileContent.index("\n") - 2]).split(", ")
    # Storing in the list vt the non-terminal symbols
    vt = (fileContent[fileContent.index("VT") + 4:fileContent.index("\n", fileContent.index("VT")) - 2]).split(", ")
    # Storing in the list grammarList the set of rules
    grammarList = (fileContent[fileContent.index("P") + 3:fileContent.index("\n", fileContent.index("P")) - 1]).split(
        ", ")
    # Splitting the rules
    for grammarRule in grammarList:
        grammarComponents = grammarRule.split(" - ")
        nextVertex = grammarComponents[1][1] if len(grammarComponents[1]) == 2 else None

        if grammarComponents[0] not in grammar:
            grammar[grammarComponents[0]] = []

        grammar[grammarComponents[0]].append((grammarComponents[1][0], nextVertex))

def FiniteAutomata(startVertex, visited, path, generatedWord, inputWord):
    global isAnswerFound

    visited[startVertex] = True
    path.append(startVertex)

    for adjacencyTuple in grammar[startVertex]:
        if generatedWord + adjacencyTuple[0] == inputWord and adjacencyTuple[1] == None:
            printPath(path, inputWord)
            isAnswerFound = True
            return
        if len(generatedWord) > len(inputWord) or adjacencyTuple[1] == None:
            continue

        FiniteAutomata(adjacencyTuple[1], visited, path, generatedWord + adjacencyTuple[0], inputWord)

    generatedWord = ""
    path.pop()
    visited[startVertex] = False

# Function for printing the path of how a word was created
def printPath(path, word):
    for vertexIndex in range(len(path)):
        if vertexIndex == 0:
            print(path[vertexIndex], end=" -> ")
            continue
        print(word[0: vertexIndex] + path[vertexIndex], end=" -> ")

    print(word)

# Setting the grammar
parseGrammar()
# Input word
print("Input string")
# Example string that will show the path is 'dabcd'
inputWord = str(input())

visited = {"S": False, "B": False, "C": False, "D": False}
FiniteAutomata("S", visited, [], '', inputWord)

if not isAnswerFound:
    print("Invalid string!")
else:
    print("Path succesfully build!")
   
