import copy

import random

from undirected_graph import UndirectedGraph


def prim(graph, start):
    colored_edges = []
    visited_nodes = []

    for node in graph.nodes:
        if node.key == start:
            visited_nodes.append(node)
            break

    while len(visited_nodes) < len(graph.nodes):
        min_cost = float('inf')
        min_edge = None
        new_node = None

        for node in visited_nodes:
            for neighbor, cost in node.neighbors:
                if neighbor not in visited_nodes:
                    if cost < min_cost:
                        min_cost = cost
                        new_node = neighbor
                        min_edge = (node.key, neighbor.key)

        visited_nodes.append(new_node)
        colored_edges.append(min_edge)

    return colored_edges


def get_edgesets_prim(iterations):
    data = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]
    edgesets = []

    for iteration in range(iterations):
        adj_matrix = data.copy()

        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] != 0:
                    w = random.choice(weights)
                    weights.remove(w)
                    adj_matrix[i][j] = w

        if adj_matrix not in edgesets:
            edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def make_question_prim(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(6)] for x in range(6)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 6 + j]

    graph = UndirectedGraph(adj_matrix, keys)
    colored_edges = prim(graph, 1)

    question_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Prim-algoritmus}} működését az alábbi gráfon, ahogy az 1-es csúcsból
            elindulva felépíti a gráf egy minimális költségű feszítőfáját! 
            \\begin{{center}}
            {graph.print_in_latex()}
            \\end{{center}}
    }}
    """

    answer_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Prim-algoritmus}} működését az alábbi gráfon, ahogy az 1-es csúcsból
            elindulva felépíti a gráf egy minimális költségű feszítőfáját! 
            \\begin{{center}}
            {graph.print_in_latex(colored_edges)}
            \\end{{center}}
    }}
    """

    return question_string, answer_string
