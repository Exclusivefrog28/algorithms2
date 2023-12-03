from bellmanford import bellmanford, print_table, get_edgesets_bellmanford, make_question_bellmanford
from bfs import get_edgesets_bfs
from dijkstra import get_edgesets_dijkstra
from floyd import make_question_floyd
from weighted_graph import Graph

with open("exam-two/bellmanford.txt", "r") as f:
    dataset = f.readlines()
    f.close()

q, a = make_question_bellmanford(dataset, "seed")

print(q)
print(a)

q, a = make_question_floyd(dataset, "seed")

print(q)
print(a)


def create_bfs_dataset():
    selected_edgesets = get_edgesets_bfs(100000, [7], 1)

    with open("exam-two/bfs.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_dijkstra_dataset():
    selected_edgesets = get_edgesets_dijkstra(100000, [7], 2)

    with open("exam-two/dijkstra.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_bellmanford_dataset():
    selected_edgesets = get_edgesets_bellmanford(1000000, [15, 16, 17])

    with open("exam-two/bellmanford.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()
