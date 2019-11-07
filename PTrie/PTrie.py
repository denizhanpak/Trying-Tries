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

class PTrie:
    def __init__(self, learning_rate, reinforcement_rate, probability_function):
        self.learning_rate = learning_rate
        self.reinforcement_rate = reinforcement_rate
 
        if probability_function in builtin:
            self.probability_function = builtin[probability_function]
        elif callable(probability_function):
            self.probability_function = probability_function
        else:
            print("Error: Probability function must be a string from the list or a valid function")

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
    
    def __repr__(self):
        return '<PTrie representation>'
            
    def __str__(self):
        return print_as_graph(self.root)

    def prune(self, threshold):
        return

    def list(self):
        to_add = parent.children.values()
        end_points = []
        for child in to_add:
            end_points.append(nx.descendants(self.network, child))
        return end_points

    def convert_to_network(self):
        parent = self.root
        to_add = deque(parent.children.values())
        parents = deque([self.root] * len(to_add)])
        self.network = nx.DiGraph()
        self.network.add_node(parent)

        while len(to_add) > 0:
            current = to_add.popleft()
            parent = parents.popleft()
            self.network.add_node(current)
            self.add_edge(parent, current, weight = current.weight)

            for child in current.children.values():
                to_add.append(child)
                parents.append(current)
            
            return self.network
