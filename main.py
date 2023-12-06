from bellmanford import bellmanford, print_table, get_edgesets_bellmanford, make_question_bellmanford
from bfs import get_edgesets_bfs
from dijkstra import get_edgesets_dijkstra
from floyd import make_question_floyd
from huffman import huffman, get_data_huffman, make_question_huffman
from prim import prim, get_edgesets_prim, make_question_prim
from undirected_graph import UndirectedGraph
from weighted_graph import Graph

with open("exam-two/huffman.txt", "r") as f:
    dataset = f.readlines()
    f.close()

q, a = make_question_huffman(dataset, 'seed')
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


def create_prim_dataset():
    selected_edgesets = get_edgesets_prim(5000)

    with open("exam-two/prim.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_huffman_dataset():
    dataset = get_data_huffman(10000)

    with open("exam-two/huffman.txt", "w") as f:
        for d in dataset:
            f.write(d + "\n")
        f.close()