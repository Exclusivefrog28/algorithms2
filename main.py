import random
from splay import SplayTree

tree = SplayTree()

data = [80, 100, 50, 30, 110, 60, 20, 70, 40, 90, 10]

random.shuffle(data)

print(f"\\documentclass{{article}}")
print(f"\\usepackage{{tikz}}")
print(f"\\usetikzlibrary{{trees}}")
print(f"\\begin{{document}}")


for x in data:
    tree.insert(x)
    tree.print_tree_in_latex()

print(f"\\end{{document}}")
