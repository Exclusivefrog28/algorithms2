import random
from bplus import BPlusTree

data = [2, 15, 20, 3, 9, 19, 12, 14, 10, 11, 13, 17, 22]

print(f"\\documentclass{{article}}")
print(f"\\usepackage{{tikz}}")
print(f"\\usetikzlibrary{{trees, arrows.meta,shapes.multipart}}")
print(f"\\usepackage{{forest}}")
print(f"\\newcommand\mpnc[3]{{\\nodepart{{one}} $#1$\\nodepart{{two}} $#2$\\nodepart{{three}} $#3$}}")
print(f"\\begin{{document}}")

tree = BPlusTree(4)

for key in data:
    if key == 22:
        pass
    tree.insert(key)
    tree.print_in_latex()
tree.delete(12)
tree.print_in_latex()
tree.delete(14)
tree.print_in_latex()
tree.delete(17)
tree.print_in_latex()
tree.delete(2)
tree.print_in_latex()


print(f"\\end{{document}}")
