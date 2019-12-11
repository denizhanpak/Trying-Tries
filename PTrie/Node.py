class Node:
    def __init__(self, char, weight):
        self.char = char
        self.weight = weight
        self.children = dict()
        self.count = 0
    
    def add_child (self, child):
        self.children[child.char] = child

    def reinforce(self, reinforcement_rate):
        self.count += 1
        self.weight += reinforcement_rate

    def print_as_graph(self, level=0):
        ret = "\t"*level+self.char+"\n"
        for child in self.children.values():
            ret += child.__str__(level+1)
        return ret

    def __str__(self):
        return self.char

    def __repr__(self):
        return '<tree node representation>'
