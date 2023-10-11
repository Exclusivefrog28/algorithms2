import random
from bplus import BPlusTree

data = [2, 17, 26, 5, 10, 21,
        14, 16, 11, 12, 13]

print(f"\\documentclass{{article}}")
print(f"\\usepackage{{tikz}}")
print(f"\\usetikzlibrary{{trees, arrows.meta,shapes.multipart}}")
print(f"\\usepackage{{forest}}")
print(f"\\newcommand\mpnc[3]{{\\nodepart{{one}} $#1$\\nodepart{{two}} $#2$\\nodepart{{three}} $#3$}}")
print(f"\\begin{{document}}")

tree = BPlusTree(4)

for key in data:
    tree.insert(key)
    tree.print_in_latex()

print(f"\\end{{document}}")
