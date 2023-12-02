import copy
import math
import random
import sys

from weighted_graph import Graph


def bellmanford(graph, start):
    result = []
    overwrites = 0

    distances = {node.key: math.inf for node in graph.nodes}
    distances[start] = 0

    predecessors = {node.key: None for node in graph.nodes}

    result.append((distances.copy().values(), predecessors.copy().values()))

    for i in range(len(graph.nodes)):
        new_distances = distances.copy()
        for node in graph.nodes:
            for neighbor in node.neighbors:
                current_distance = distances[node.key] + neighbor[1]
                if current_distance < distances[neighbor[0].key]:
                    new_distances[neighbor[0].key] = current_distance
                    predecessors[neighbor[0].key] = node.key

        for key, value in distances.items():
            if value != new_distances[key]:
                overwrites += 1
                if i == len(graph.nodes) - 1:
                    return [], True, 0

        distances = new_distances

        if i != len(graph.nodes) - 1:
            result.append((distances.copy().values(), predecessors.copy().values()))

    return result, False, overwrites


def print_table(steps):
    table = """\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
        \\hline
        \\ & \\multicolumn{8}{c|}{d} & \\multicolumn{8}{c|}{\\Pi}\\\\
        \\hline
        & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8\\\\
        \\hline\n
        """
    for index, step in enumerate(steps):
        d = ' & '.join(map(lambda x: '∞' if x == float('inf') else str(x), step[0]))
        pi = ' & '.join(map(lambda x: 'NIL' if x is None else str(x), step[1]))

        table += f"         {index} & {d} & {pi}\\\\\n"
        table += '          \\hline\n'

    table += '      \\end{tabular}'

    return table


def get_edgesets_bellmanford(iterations, overwrites):
    data = [
        [0, 0, 0, 0, 2, 0, 0, 3],
        [0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 2, 0],
        [0, 3, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0]
    ]
    keys = [1, 2, 3, 4, 5, 6, 7, 8]
    edgesets = []

    percent = iterations / 100

    for iteration in range(iterations):
        adj_matrix = data.copy()
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] != 0:
                    if random.random() < 0.1:
                        adj_matrix[i][j] = 0
                        adj_matrix[j][i] = (random.randint(2, 9) if random.random() < .5 else random.randint(-3, -1))
        graph = Graph(adj_matrix, keys)
        result, negative_cycle, current_overwrites = bellmanford(graph, 1)

        if iteration % percent == 0:
            sys.stdout.write(f"\r{iteration / percent}% - {len(edgesets)} graphs")
            sys.stdout.flush()

        if not negative_cycle and current_overwrites in overwrites and result[-1][0] != result[-2][0]:
            if adj_matrix not in edgesets:
                edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def make_question_bellmanford(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6, 7, 8]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(8)] for x in range(8)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 8 + j]

    graph = Graph(adj_matrix, keys)
    result, negative_cycle, overwrites = bellmanford(graph, 1)

    question_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Bellman—Ford-algoritmus}} működését az alábbi gráfon ahogy megtalálja az 1-es csúcsból, mint
            forrásból a többi csúcsba vezető legrövidebb utakat! Kövessük nyomon a távolságokat tartalmazó (d) és a szomszédságokat
            nyilvántartó (Π) tömbök tartalmának változását az algoritmus futása során! 
            \\begin{{center}}
            {graph.print_in_latex()}
            \\end{{center}}
    }}
    """

    answer_string = f"""\\item{{
            Szemléltessünk a \\textbf{{Bellman—Ford-algoritmus}} működését az alábbi gráfon ahogy megtalálja az 1-es csúcsból, mint
            forrásból a többi csúcsba vezető legrövidebb utakat! Kövessük nyomon a távolságokat tartalmazó (d) és a szomszédságokat
            nyilvántartó (Π) tömbök tartalmának változását az algoritmus futása során!
            \\begin{{center}}
            {print_table(result)}
            \\end{{center}}
    }}
    """

    return question_string, answer_string
