from helpful import *
from PDA_parser import *

def makeTerminalNFA(char):
    dicts = [{},{},{},{}]
    dicts[0]["eps"] = "1 "
    dicts[1][str(char)] = "2 "
    dicts[2]["eps"] = "3 "

    finalStates = [3]
    alpha = set()
    alpha.add("eps")
    alpha.add(str(char))

    return NFA(dicts, finalStates, alpha)

def makeEmptyNFA():
    dicts = []
    finalStates = []
    alpha = set()
    return NFA(dicts, finalStates, alpha)


def makeNFA(tree):

    if len(tree.nodes) == 0:
        return makeEmptyNFA()

    nfaCrt = None
    i = 0
    while i < len(tree.nodes):
        if tree.nodes[i].type == 't':
            nfaCrt = makeTerminalNFA(tree.nodes[i].data)
            if tree.nodes[i].kleen:
                nfaCrt = kleenS(nfaCrt)
            i = i + 1

      
        elif tree.nodes[i].type == 'n':
            nfaCrt = makeNFA(tree.nodes[i])
            if tree.nodes[i].kleen:
                nfaCrt = kleenS(nfaCrt)
            i = i + 1


        elif tree.nodes[i].type == 'o':
            i = i + 1
            aux = None
            if tree.nodes[i].type == 't':
                aux = makeTerminalNFA(tree.nodes[i].data)
            if tree.nodes[i].type == 'n':
                aux = makeNFA(tree.nodes[i])
            
            if tree.nodes[i].kleen:
                aux = kleenS(aux)
            
            if tree.nodes[i - 1].data == ".":
                nfaCrt = concatNFA(nfaCrt, aux)
            if tree.nodes[i - 1].data == "|":
                nfaCrt = intersection(nfaCrt, aux)
            
            i = i + 1

    return nfaCrt


def intersection(n1, n2):
    size1 = len(n1.dicts)
    size2 = len(n2.dicts)

    if size1 == 0:
        return n2
    if size2 == 0:
        return n1

    newDicts = [{},{}]
    newDicts[0]["eps"] = "1 "
    newDicts[1]["eps"] = "2 "
    newDicts[1]["eps"] += str(size1 + 2) + " "

    for i in range(0,len(n1.dicts)):
        d = n1.dicts[i]
        auxDict = {}
        for key in d.keys():
            l = id_to_states(d[key])
            l = map(lambda x: x + 2, l)
            aux = states_to_id(l)
            auxDict[key] = aux
        newDicts.append(auxDict)
    
    for i in range(0,len(n2.dicts)):
        d = n2.dicts[i]
        auxDict = {}
        for key in d.keys():
            l = id_to_states(d[key])
            l = map(lambda x: x + size1 + 2, l)
            aux = states_to_id(l)
            auxDict[key] = aux
        newDicts.append(auxDict)

    newDicts[size1 + 1]["eps"] = str(size1 + size2 + 2) + " "
    newDicts[size1 + size2 + 1]["eps"] = str(size1 + size2 + 2) + " "

    aux = {}
    aux["eps"] = str(size1 + size2 + 3) + " "
    newDicts.append(aux)
    newDicts.append({})

    finalStates = [size1 + size2 + 3]
    alpha = n1.alpha.union(n2.alpha)

    return NFA(newDicts, finalStates, alpha)


def concatNFA(n1, n2):
    
    size1 = len(n1.dicts)

    dicts2 = []

    for i in range(0,len(n2.dicts)):
        d = n2.dicts[i]
        auxDict = {}
        for key in d.keys():
            l = id_to_states(d[key])
            l = map(lambda x: x + size1, l)
            aux = states_to_id(l)
            auxDict[key] = aux
        dicts2.append(auxDict)

    n1.dicts[-1]["eps"]  = str(size1) + " "
    n1.dicts += dicts2

    n1.final_states = [len(n1.dicts) - 1]
    n1.alpha = n1.alpha.union(n2.alpha)

    return n1

def kleenS(nfa):
    size = len(nfa.dicts)

    if "eps" not in nfa.dicts[1]:
        nfa.dicts[1]["eps"] = ""

    if "eps" not in nfa.dicts[size - 2]:
        nfa.dicts[size - 2]["eps"] = ""
        
    nfa.dicts[1]["eps"] += str(size - 2) + " "
    nfa.dicts[size - 2]["eps"] += str(1) + " "

    return nfa



pda = PDA_parser()
tree = pda.parseExpression("((ba)d**)")
nf = makeNFA(tree)
print(nf)
print(transform(nf))
