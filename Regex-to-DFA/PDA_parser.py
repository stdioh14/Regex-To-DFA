from helpful import NFA

class PDA_parser:
    def __init__(self):

        self.stack = [Node('^', 'n')]

    def parseExpression(self, word):
        
        result = None

        print(self.stack[-1].data)
        #print(word)

        while self.stack[-1].data != '^' or word != "":
            #print("aici")
            #print(word)


            if self.stack[-1].data == '^':
                #print("?")
                self.stack.append(Node('S', 's'))
                self.stack[-1].type = 's'
            
            if word != "":
                if word[0] == '(':
                    if self.stack[-1].type != 'o' and self.stack[-1].complete:
                        self.stack.append(Node('.', 'o'))
                        self.stack[-1].complete = True 
                    self.stack.append(Node('E', 'n'))
                    word = word[1:len(word)] 
                elif word[0] >= 'a' and word[0] <= 'z':
                    if self.stack[-1].type != 'o' and self.stack[-1].complete:
                        self.stack.append(Node('.', 'o'))
                        self.stack[-1].complete = True 
                    self.stack.append(Node(word[0], 't'))
                    word = word[1:len(word)]
                    self.stack[-1].complete = True
                elif word[0] == '|':
                    self.stack.append(Node(word[0], 'o'))
                    word = word[1:len(word)]
                    self.stack[-1].complete = True
                elif word[0] == '*':
                    self.stack[-1].kleen = True
                    word = word[1:len(word)]
                elif word[0] == ')':
                    nodes = []
                    
                    while self.stack[-1].complete:
                        nodes.insert(0, self.stack.pop())
                    
                    self.stack[-1].nodes = nodes
                    self.stack[-1].complete = True
                    #print(self.stack[-1].data)
                    
                    word = word[1:len(word)]



            #print(word)


            if word == "":
                nodes = []
                while self.stack[-1].type != 's':
                    print(self.stack[-1].data)
                    node = self.stack.pop()
                    nodes.insert(0, node)
                
                self.stack[-1].nodes = nodes
                self.stack[-1].complete = True

                result = self.stack.pop()
        
        return result



            


class Node:

    def __init__(self, data, node_type):

        self.nodes = []
        self.type = node_type
        self.kleen = False
        self.complete = False
        self.data = data

    def __str__(self): 
        
        string = "eu sunt" + self.data + "si am tipul: " + self.type + "\n"
        for i in range(0, len(self.nodes)):
            string += str(self.nodes[i])
        return string

      



