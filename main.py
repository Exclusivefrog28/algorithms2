from weighted_graph import Graph
from bfs import get_edgesets_bfs
from dijkstra import dijkstra, print_table

adj_matrix = [
    [0, 3, 0, 0, 0, 0],
    [0, 0, 0, 4, 10, 13],
    [0, 0, 0, 0, 0, 0],
    [5, 0, 7, 0, 2, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0]
]

graph = Graph(adj_matrix, [1, 2, 3, 4, 5, 6])
result = dijkstra(graph, 1)
print(print_table(result))


def create_bfs_dataset():
    data = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0]
    ]

    selected_edgesets = get_edgesets_bfs(data, 100000, [7], 1)

    with open("exam-two/bfs.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()
