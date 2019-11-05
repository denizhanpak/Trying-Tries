import Node
import PTrie


corpus = "manly man mans man manning man"
trie = PTrie(1,1,probability_function_simple)
print(trie.run(corpus))
