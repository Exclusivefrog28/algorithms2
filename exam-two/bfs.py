import copy
import math
import random


class GraphNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value else key
        self.neighbors = []


def print_dependencies():
    print("\\usepackage{tikz}")
    print("\\usetikzlibrary{graphs,graphdrawing,arrows.meta}")
    print("\\usegdlibrary{circular,force,layered,routing}")
    print(
        "\\tikzset{graphs/simpleer/.style={nodes={draw, circle},node distance=2.5cm, nodes={minimum size=2em}}}")


class Graph:
    def __init__(self, adj_matrix, keys):
        self.nodes = []
        for i, row in enumerate(adj_matrix):
            self.nodes.append(GraphNode(keys[i]) if keys else GraphNode(i))
        for i, row in enumerate(adj_matrix):
            for j, value in enumerate(row):
                if value > 0:
                    self.nodes[i].neighbors.append(self.nodes[j])

    def breadth_first_search(self, decreasing_order=False):
        self.nodes.sort(key=lambda node: node.key, reverse=decreasing_order)

        visited = []
        queue = []
        d = {}
        pi = {}

        result = []

        for node in self.nodes:
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
                    if neighbor.key not in visited:
                        visited.append(neighbor.key)
                        queue.append(neighbor)
                        d[neighbor.key] = d[current_node.key] + 1
                        pi[neighbor.key] = current_node.key

                save_step(queue, visited, d, pi)

        components = 0

        for node in self.nodes:
            if node.key not in visited:
                bfs(node)
                components += 1

        return result, components

    def print_in_latex(self):
        graph_string = f"""\\begin{{tikzpicture}}[>=Latex]
            \\graph[simpleer, spring layout]{{
            {self.print_edges()}
            }};
            \\end{{tikzpicture}}"""

        return graph_string

    def print_edges(self):
        edges_string = ""
        for node in self.nodes:
            for neighbor in node.neighbors:
                edges_string += f"\"{node.value}\" -> \"{neighbor.value}\", "
        return edges_string


def print_table(steps):
    print('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}')
    print('\\hline')
    print(
        '\\multirow{2}{4em}{S} & \\multirow{2}{4em}{ELÉRT} & \\multicolumn{6}{c|}{d} & \\multicolumn{6}{c|}{\\Pi}\\\\')
    print('\\cline{3-14}')
    print('& & 1 & 2 & 3 & 4 & 5 & 6 & 1 & 2 & 3 & 4 & 5 & 6\\\\')
    print('\\hline')
    for step in steps:
        queue = ', '.join(map(str, step[0]))
        visited = ', '.join(map(str, step[1]))
        d = ' & '.join(map(str, step[2]))
        pi = ' & '.join(map(str, step[3]))

        print(f"{queue} & {visited} & {d} & {pi}\\\\")
        print('\\hline')

    print('\\end{tabular}')


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



    # return question_string, answer_string, answer
