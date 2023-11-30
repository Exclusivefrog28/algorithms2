import copy
import math
import random
from weighted_graph import Graph


def breadth_first_search(graph, decreasing_order=False):
    graph.nodes.sort(key=lambda node: node.key, reverse=decreasing_order)

    visited = []
    queue = []
    d = {}
    pi = {}

    result = []

    for node in graph.nodes:
        d[node.key] = "∞"
        pi[node.key] = None

    def save_step(queue, visited, d, pi):
        queue_keys = []
        for node in queue:
            queue_keys.append(node.key)
        result.append([queue_keys.copy(), visited.copy(), d.copy().values(), pi.copy().values()])

    def bfs(node):
        visited.append(node.key)
        queue.append(node)
        d[node.key] = 0
        save_step(queue, visited, d, pi)
        while not len(queue) == 0:
            current_node = queue.pop(0)
            for neighbor in current_node.neighbors:
                if neighbor[0].key not in visited:
                    visited.append(neighbor[0].key)
                    queue.append(neighbor[0])
                    d[neighbor[0].key] = d[current_node.key] + 1
                    pi[neighbor[0].key] = current_node.key

            save_step(queue, visited, d, pi)

    components = 0

    for node in graph.nodes:
        if node.key not in visited:
            bfs(node)
            components += 1

    return result, components


def print_table(steps):
    table = """\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
        \\hline
        \\multirow{2}{*}{ S } & \\multirow{2}{*}{ELÉRT} & \\multicolumn{6}{c|}{d} & \\multicolumn{6}{c|}{\\Pi}\\\\
        \\cline{3-14}
        & & 1 & 2 & 3 & 4 & 5 & 6 & 1 & 2 & 3 & 4 & 5 & 6\\\\
        \\hline\n
        """
    for step in steps:
        queue = ', '.join(map(str, step[0]))
        visited = ', '.join(map(str, step[1]))
        d = ' & '.join(map(str, step[2]))
        pi = ' & '.join(map(lambda x: 'NIL' if x is None else str(x), step[3]))

        table += f"         {queue} & {visited} & {d} & {pi}\\\\\n"
        table += '          \\hline\n'

    table += '      \\end{tabular}'

    return table


def get_edgesets_bfs(data, iterations, steps, components):
    keys = [1, 2, 3, 4, 5, 6]
    edgesets = []

    for iteration in range(iterations):
        adj_matrix = data.copy()
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] == 1:
                    if random.random() < math.sqrt(.5):
                        adj_matrix[i][j] = 0
                        adj_matrix[j][i] = 1
        graph = Graph(adj_matrix, keys)
        result, current_components = graph.breadth_first_search()

        if len(result) in steps and components == current_components:
            if adj_matrix not in edgesets:
                edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def make_question_bfs(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(6)] for x in range(6)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 6 + j]

    graph = Graph(adj_matrix, keys)
    result, components = breadth_first_search(graph)

    question_string = f"""\\item{{
            Járjuk be az 1-es csúcsból indulva \\textbf{{szélességi bejárással}} az alábbi gráfot!
            A csúcsok szomszédjainak feldolgozási sorrendje legyen a csúcsok címkéiben nagyság szerint növekedően rendezett.
            Táblázatban jelöljük lépésenként a sor, a bejárva tömb, valamint a távolsági (d) és szomszédsági (Π) listák tartalmát.\\\\[1em]
            \\begin{{center}}
            {graph.print_in_latex()}
            \\end{{center}}
    }}
    """

    answer_string = f"""\\item{{
            Járjuk be az 1-es csúcsból indulva \\textbf{{szélességi bejárással}} az alábbi gráfot!
            A csúcsok szomszédjainak feldolgozási sorrendje legyen a csúcsok címkéiben nagyság szerint növekedően rendezett.
            Táblázatban jelöljük lépésenként a sor, a bejárva tömb, valamint a távolsági (d) és szomszédsági (Π) listák tartalmát.\\\\[1em]
            \\begin{{center}}
            {print_table(result)}
            \\end{{center}}
    }}
    """

    return question_string, answer_string
