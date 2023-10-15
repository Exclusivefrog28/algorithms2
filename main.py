import random
from graph import Graph, print_dependencies

graph_keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# adj_matrix = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#               [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
#               [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
#               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]

adj_matrix = [[0, 1, 0, 1, 0],
              [0, 0, 0, 0, 1],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 1],
              [0, 0, 1, 0, 0]]

print(f"\\documentclass{{article}}")
print_dependencies()
print(f"\\begin{{document}}")

graph = Graph(adj_matrix, graph_keys)
graph.print_in_latex()
reduced_graph = graph.reduced()
reduced_graph.print_in_latex()
print(f"\\end{{document}}")
