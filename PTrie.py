import random 
import math

class Node:
    def __init__(self, char, weight):
        self.char = char
        self.weight = weight
        self.children = dict()
    
    def add_child (self, child):
        self.children[child.char] = child

    def reinforce(self, reinforcement_rate):
        self.weight *= reinforcement_rate

    def __str__(self, level=0):
        ret = "\t"*level+self.char+"\n"
        for child in self.children.values():
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
    

class PTrie:
    def __init__(self, learning_rate, reinforcement_rate, probability_function):
        self.learning_rate = learning_rate
        self.reinforcement_rate = reinforcement_rate
        self.probability_function = probability_function
        self.root = Node("ROOT", None)


    def run(self, corpus):
        context = self.root
        for character in corpus:

            #Skip non alphanumeric characters except ' for 
            if character in " ,.;!?":
                context = self.root
                continue

            #Define the rules for adding a new node
            if context == self.root:
                learning = 1
                reinforcement = 1
            else:
                learning = self.learning_rate
                reinforcement = self.reinforcement_rate

            #Add new child node to context
            if character not in context.children:
                node = Node(character, learning)
                context.add_child(node)

            #Reinforce weights from context to child
            else:
                node = context.children[character]
                node.reinforce(reinforcement)

            #Probabilistically move in context or return to root
            probability = self.probability_function(node.weight)
            if random.uniform(0, 1) <= probability:
                context = node
            else:
                context = self.root

        return self.root
            
def probability_function_simple(number):
    return number/(number + 1)

def probability_function_sigmoid(number):
    return 1/(1+math.exp(-number))

def probability_function_sigmoid_translate(number, shift):
    return 1/(1+math.exp(shift - number))

def deterministic_function(number):
    return 1

corpus = "manly man mans man manning man"
trie = PTrie(1,1,probability_function_simple)
print(trie.run(corpus))
