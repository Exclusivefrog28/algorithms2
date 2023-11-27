from bfs import Graph

adj_matrix = [
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0]
]

graph = Graph(adj_matrix, [1, 2, 3, 4, 5])

print('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|}')
print('\\hline')
print('\\multirow{2}{4em}{S} & \\multirow{2}{4em}{ELÉRT} & \\multicolumn{5}{|c|}{d} & \\multicolumn{5}{|c|}{\\Pi}\\\\')
print('& & 1 & 2 & 3 & 4 & 5 & 1 & 2 & 3 & 4 & 5\\\\')
print('\\hline')

graph.breadth_first_search()

print('\\end{tabular}')
