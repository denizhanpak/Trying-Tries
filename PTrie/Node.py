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
    

