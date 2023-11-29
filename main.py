from bfs import Graph, print_table, get_edgesets_bfs

adj_matrix = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0]
]


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


create_bfs_dataset()
