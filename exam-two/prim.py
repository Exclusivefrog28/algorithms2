import copy

import random

from undirected_graph import UndirectedGraph


def prim(graph, start):
    colored_edges = []
    visited_nodes = []
    colored_edges_history = []
    visited_nodes_history = []

    for node in graph.nodes:
        if node.key == start:
            visited_nodes.append(node)
            break

    visited_nodes_history.append(copy.deepcopy(visited_nodes))
    colored_edges_history.append(copy.deepcopy(colored_edges))

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
        visited_nodes_history.append(copy.deepcopy(visited_nodes))
        colored_edges_history.append(copy.deepcopy(colored_edges))

    return visited_nodes_history, colored_edges_history


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

def print_table(visited_nodes, colored_edges):
    table = """\\begin{tabular}{c|c}
        U & F\\\\
        \\hline\n
        """

    for index, node in enumerate(visited_nodes):
        step = (visited_nodes[index], colored_edges[index])
        visited = ', '.join(map(lambda x: str(x.key), step[0]))
        colored = ', '.join(map(lambda x: f"({x[0]},{x[1]})", step[1]))

        table += f"         {visited} & {colored}\\\\\n"

    table += '      \\end{tabular}'

    return table

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
    visited_nodes, colored_edges = prim(graph, 1)

    question_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Prim-algoritmus}} működését, ahogy az 1-es csúcsból elindulva 
            felépíti az alábbi gráf egy minimális költségű feszítőfáját! Adjuk meg az iterációs lépesekben
            a feszítőfa csúcsait (U) és éleit (F).
            \\begin{{center}}
            {graph.print_in_latex()}
            \\hfill
            \\begin{{tabular}}{{x{{2cm}}|x{{4cm}}}}
            U & F\\\\
            \\hline
            1 & \\\\
            \\hdashline
              & \\\\
             \\hdashline
              & \\\\
             \\hdashline
             & \\\\
             \\hdashline
             & \\\\
             \\hdashline
             & \\\\
          \\end{{tabular}}
            \\end{{center}}
    }}
    """

    answer_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Prim-algoritmus}} működését, ahogy az 1-es csúcsból elindulva 
            felépíti az alábbi gráf egy minimális költségű feszítőfáját! Adjuk meg az iterációs lépesekben
            a feszítőfa csúcsait (U) és éleit (F).
            \\begin{{center}}
            {graph.print_in_latex(colored_edges[-1])}
            \\hfill
            {print_table(visited_nodes, colored_edges)}
            \\end{{center}}
    }}
    """

    return question_string, answer_string
