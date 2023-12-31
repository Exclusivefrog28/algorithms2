import copy
import math
import random
import sys

from weighted_graph import Graph


def floyd(graph):
    adj_matrix = [[0.0 for y in range(6)] for x in range(6)]
    predecessors = [['\\emptyset' for y in range(6)] for x in range(6)]

    for node in graph.nodes:
        for neighbor in node.neighbors:
            adj_matrix[node.key - 1][neighbor[0].key - 1] = neighbor[1]
        for i in range(len(adj_matrix[node.key - 1])):
            if adj_matrix[node.key - 1][i] == 0 and i != (node.key - 1):
                adj_matrix[node.key - 1][i] = float('inf')

    distance_matrices = [copy.deepcopy(adj_matrix)]
    predecessor_matrices = [copy.deepcopy(predecessors)]

    for k in range(len(graph.nodes)):
        for i in range(len(graph.nodes)):
            for j in range(len(graph.nodes)):
                distance_with_k = adj_matrix[i][k] + adj_matrix[k][j]
                if distance_with_k < adj_matrix[i][j]:
                    adj_matrix[i][j] = distance_with_k
                    predecessors[i][j] = str(k + 1)
        distance_matrices.append(copy.deepcopy(adj_matrix))
        predecessor_matrices.append(copy.deepcopy(predecessors))

    return distance_matrices, predecessor_matrices


def print_matrix(matrix, dtype, name, endline=''):
    string = f"${name} =$ $\\left[\\,\\begin{{NiceArray}}{{x{{0.5cm}}:x{{0.5cm}}:x{{0.5cm}}:x{{0.5cm}}:x{{0.5cm}}:x{{0.5cm}}}}\n"
    for row in matrix:
        row = map(lambda x: str(int(x) if dtype == 'int' else x) if x != float('inf') else '\\infty', row)
        string += f"{' & '.join(row)}\\\\\n"
        if row != matrix[-1]:
            string += "\\hdashline\n"

    string += f"\\end{{NiceArray}}\\,\\right]${endline}"
    return string


def make_question_floyd(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(6)] for x in range(6)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 6 + j]

    graph = Graph(adj_matrix, keys)
    F, P = floyd(graph)

    question_string = f"""\\item{{
            Szemléltessük a \\textbf{{Floyd algoritmus}} működését a 3. feladat gráfján! Adjuk meg az iterációs
            lépésekben adódó F távolsági és P szomszédsági mátrixokat!\\\\
    }}
    """

    matrices = ""
    for i in range(len(F)):
        endline = "\\\\"
        matrices += f"{print_matrix(F[i], 'int', 'F_' + str(i))}\n\\hfill\n{print_matrix(P[i], 'string', 'P_' + str(i), endline)}\n\\vspace{{0.15cm}}\\\\\n"

    answer_string = f"""\\item{{
            Szemléltessük a \\textbf{{Floyd algoritmus}} működését a 3. feladat gráfján! Adjuk meg az iterációs
            lépésekben adódó F távolsági és P szomszédsági mátrixokat!\\\\
            \\newpage
            {matrices}
    }}
    """

    return question_string, answer_string
