import copy
import math
import random

from weighted_graph import Graph


def dijkstra(graph, start):
    result = []
    overwrites = 0

    distances = {}
    previous_nodes = {}
    unvisited_nodes = copy.deepcopy(graph.nodes)

    for i, node in enumerate(unvisited_nodes):
        distances[node.key] = float('inf')
        previous_nodes[node] = None
        if node.key == start:
            distances[node.key] = 0
            temp = unvisited_nodes[0]
            unvisited_nodes[0] = unvisited_nodes[i]
            unvisited_nodes[i] = temp

    visited_nodes = []

    result.append((visited_nodes.copy(), distances.copy().values(), previous_nodes.copy().values()))

    while len(unvisited_nodes) > 0:
        current_node = unvisited_nodes[0]
        for node in unvisited_nodes:
            if distances[node.key] < distances[current_node.key]:
                current_node = node

        visited_nodes.append(current_node)
        unvisited_nodes.remove(current_node)
        for neighbor in current_node.neighbors:
            temp_distance = distances[current_node.key] + neighbor[1]
            if temp_distance < distances[neighbor[0].key]:
                if distances[neighbor[0].key] != float('inf'):
                    overwrites += 1
                distances[neighbor[0].key] = temp_distance
                previous_nodes[neighbor[0]] = current_node
                temp = unvisited_nodes[0]
                unvisited_nodes[0] = unvisited_nodes[unvisited_nodes.index(neighbor[0])]
                unvisited_nodes[unvisited_nodes.index(neighbor[0])] = temp

        result.append((visited_nodes.copy(), distances.copy().values(), previous_nodes.copy().values()))

    return result, overwrites


def print_table(steps):
    table = """\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
        \\hline
        \\multirow{2}{*}{KÉSZ} & \\multicolumn{8}{c|}{d} & \\multicolumn{8}{c|}{\\Pi}\\\\
        \\cline{2-17}
        & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8\\\\
        \\hline\n
        """
    for step in steps:
        visited = ', '.join(map(lambda x: str(x.key), step[0]))
        d = ' & '.join(map(lambda x: '∞' if x == float('inf') else str(x), step[1]))
        pi = ' & '.join(map(lambda x: 'NIL' if x is None else str(x.key), step[2]))

        table += f"         {visited} & {d} & {pi}\\\\\n"
        table += '          \\hline\n'

    table += '      \\end{tabular}'

    return table


def get_edgesets_dijkstra(iterations, overwrites):
    data = [
        [0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0]
    ]
    keys = [1, 2, 3, 4, 5, 6, 7, 8]
    edgesets = []

    for iteration in range(iterations):
        adj_matrix = data.copy()
        remaining_weights = list(range(2, 15))
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] > 0:
                    if random.random() < math.sqrt(.5):
                        adj_matrix[i][j] = 0
                        adj_matrix[j][i] = 1

        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] > 0:
                    adj_matrix[i][j] = random.choice(remaining_weights)
                    remaining_weights.remove(adj_matrix[i][j])

        graph = Graph(adj_matrix, keys)
        result, current_overwrites = dijkstra(graph, 1)
        if current_overwrites in overwrites and float('inf') not in result[-1][1]:
            if adj_matrix not in edgesets:
                edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def make_question_dijkstra(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6, 7, 8]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(8)] for x in range(8)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 8 + j]

    graph = Graph(adj_matrix, keys)
    result, overwrites = dijkstra(graph, 1)

    question_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Dijkstra-algoritmus}} működését az alábbi gráfon ahogy megtalálja az 1-es csúcsból, mint
            forrásból a többi csúcsba vezető legrövidebb utakat! Kövessük nyomon a távolságokat tartalmazó (d) és a 
            szomszédságokat nyilvántartó (Π) tömbök tartalmának változását az algoritmus futása során! 
            \\begin{{center}}
            {graph.print_in_latex()}
            \\end{{center}}
    }}
    """

    answer_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Dijkstra-algoritmus}} működését az alábbi gráfon ahogy megtalálja az 1-es csúcsból, mint
            forrásból a többi csúcsba vezető legrövidebb utakat! Kövessük nyomon a távolságokat tartalmazó (d) és a 
            szomszédságokat nyilvántartó (Π) tömbök tartalmának változását az algoritmus futása során!
            \\begin{{center}}
            {print_table(result)}
            \\end{{center}}
    }}
    """

    return question_string, answer_string
