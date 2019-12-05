import random 
import math
import Node
import networkx as nx
from collections import deque

def probability_function_simple(number):
    return number/(number + 1)

def probability_function_sigmoid(number):
    return 1/(1+math.exp(-number))

def probability_function_sigmoid_translate(number, shift):
    return 1/(1+math.exp(shift - number))

def deterministic_function(number):
    return 1

builtin = {"simple":probability_function_simple, "sigmoid":probability_function_sigmoid, 
        "sigmoid_translated":probability_function_sigmoid_translate, "deterministic":deterministic_function}

class Trie:
    def __init__(self, learning_rate, reinforcement_rate, probability_function):
        self.learning_rate = learning_rate
        self.reinforcement_rate = reinforcement_rate
 
        if probability_function in builtin:
            self.probability_function = builtin[probability_function]
        elif callable(probability_function):
            self.probability_function = probability_function
        else:
            print("Error: Probability function must be a string from the list or a valid function f:Z->[0,1]")

        self.root = Node.Node("ROOT", None)

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
                node = Node.Node(character, learning)
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
    
    def __repr__(self):
        return '<PTrie representation>'
            
    def __str__(self):
        return print_as_graph(self.root)

    #This function will reduce the size of the tree by removing low probability connections
    def prune(self, threshold):
        return

    #Returns a dictionary which has all words and their likelihood measures implemented using DFS
    def list(self):
        #All morphemes start with children of roots
        first_letters = self.root.children.values()
        all_strings = []

        for starting_letter in first_letters:
            all_strings.append(self.get_morphemes(starting_letter))

        return all_strings

    #Returns all possible morpheme children for a given node in the tree
    def get_morphemes(self, node, previous_letters):

        if len(node.children) == 0:
            return ([node.char], [node.weight])
        
        possible_morphemes = []
        possible_weights = []

        for child in node.children:
            child_node = node.children[child]
            successive_letters, successive_weights = get_morphemes(child_node, current_morphem)
            
            for morpheme, weight in zip(successive_letters, successive_weights):
                possible_morphemes.append(self.char + morpheme)
                possible_weights.append(weight * node.weight)

        return (possible_morphemes, possible_weights)

corpus = "manly man mans man manning man"
trie = Trie(1,1,"simple")
print(trie.run(corpus))
print(trie.list())
