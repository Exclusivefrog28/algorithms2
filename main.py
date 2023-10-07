import random
from avl import AVLTree

data = [80, 100, 50, 30, 110, 60, 20, 70, 40, 90, 10]

# print(f"\\documentclass{{article}}")
# print(f"\\usepackage{{tikz}}")
# print(f"\\usetikzlibrary{{trees}}")
# print(f"\\begin{{document}}")

for i in range(1000):
    tree = AVLTree()
    random.shuffle(data)
    for x in data:
        tree.insert(x)
    if tree.single_rotations == 3 and tree.double_rotations == 2:
        print(data)

# print(f"\\end{{document}}")
