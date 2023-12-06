from bellmanford import get_edgesets_bellmanford, make_question_bellmanford
from bfs import get_edgesets_bfs, make_question_bfs
from dijkstra import get_edgesets_dijkstra, make_question_dijkstra
from floyd import make_question_floyd
from huffman import get_data_huffman, make_question_huffman
from prim import get_edgesets_prim, make_question_prim
from quicksearch import get_data_quicksearch, make_question_quicksearch

seed = 'seed'

with open("exam-two/bfs.txt", "r") as f:
    bfs_dataset = f.readlines()
    f.close()
with open("exam-two/dijkstra.txt", "r") as f:
    dijkstra_dataset = f.readlines()
    f.close()
with open("exam-two/bellmanford.txt", "r") as f:
    bellmanford_dataset = f.readlines()
    f.close()
with open("exam-two/prim.txt", "r") as f:
    prim_dataset = f.readlines()
    f.close()
with open("exam-two/huffman.txt", "r") as f:
    huffman_dataset = f.readlines()
    f.close()
with open("exam-two/quicksearch.txt", "r") as f:
    quicksearch_dataset = f.readlines()
    f.close()

bfs_q, bfs_a = make_question_bfs(bfs_dataset, seed)
dijkstra_q, dijkstra_a = make_question_dijkstra(dijkstra_dataset, seed)
bellmanford_q, bellmanford_a = make_question_bellmanford(bellmanford_dataset, seed)
floyd_q, floyd_a = make_question_floyd(bellmanford_dataset, seed)
prim_q, prim_a = make_question_prim(prim_dataset, seed)
huffman_q, huffman_a = make_question_huffman(huffman_dataset, seed)
quicksearch_q, quicksearch_a = make_question_quicksearch(quicksearch_dataset, seed)

print(bfs_a)
print(dijkstra_a)
print(bellmanford_a)
print(floyd_a)
print(prim_a)
print(huffman_a)
print(quicksearch_a)

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


def create_quicksearch_dataset():
    dataset = get_data_quicksearch(10000000, [10, 11, 12], 1)

    with open("exam-two/quicksearch.txt", "w") as f:
        for d in dataset:
            f.write(d + "\n")
        f.close()
