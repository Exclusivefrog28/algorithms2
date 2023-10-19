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

    def depth_first_search(self, decreasing_order=False):
        self.nodes.sort(key=lambda node: node.key, reverse=decreasing_order)

        visited = {}
        depth_numbers, finish_numbers = {}, {}
        depth, finish = 0, 0
        tree_edges, back_edges, forward_edges, cross_edges = [], [], [], []

        for node in self.nodes:
            visited[node.key] = False
            depth_numbers[node.key] = 0
            finish_numbers[node.key] = 0
            node.neighbors.sort(key=lambda neighbor: neighbor.key, reverse=decreasing_order)

        def dfs(node):
            visited[node.key] = True
            nonlocal depth, depth_numbers, finish, finish_numbers
            depth += 1
            depth_numbers[node.key] = depth
            for neighbor in node.neighbors:

                if depth_numbers[neighbor.key] == 0:
                    nonlocal tree_edges
                    tree_edges.append((node.key, neighbor.key))
                elif depth_numbers[neighbor.key] > depth_numbers[node.key]:
                    nonlocal forward_edges
                    forward_edges.append((node.key, neighbor.key))
                elif depth_numbers[neighbor.key] <= depth_numbers[node.key] and finish_numbers[neighbor.key] == 0:
                    nonlocal back_edges
                    back_edges.append((node.key, neighbor.key))
                elif depth_numbers[neighbor.key] < depth_numbers[node.key] and finish_numbers[neighbor.key] > 0:
                    nonlocal cross_edges
                    cross_edges.append((node.key, neighbor.key))

                if not visited[neighbor.key]:
                    dfs(neighbor)

            finish += 1
            finish_numbers[node.key] = finish

        for node in self.nodes:
            if not visited[node.key]:
                dfs(node)

        return depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges

    def reduce_to_dag(self, decreasing=False):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search(
            decreasing_order=decreasing)
        for node in self.nodes:
            node.neighbors = [neighbor for neighbor in node.neighbors if not (node.key, neighbor.key) in back_edges]

    def reduce_to_tree(self, decreasing=False):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search(
            decreasing_order=decreasing)
        for node in self.nodes:
            node.neighbors = [neighbor for neighbor in node.neighbors if (node.key, neighbor.key) in tree_edges]

    def topological_order(self):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search()
        node_keys = [node.key for node in self.nodes]
        node_keys.sort(key=lambda key: finish_numbers[key], reverse=True)
        return node_keys

    def flip_edges(self):
        new_nodes = []
        for node in self.nodes:
            new_node = GraphNode(node.key)
            new_nodes.append(new_node)

        for node in self.nodes:
            for neighbor in node.neighbors:
                new_node = next(x for x in new_nodes if x.key == neighbor.key)
                new_neighbor = next(x for x in new_nodes if x.key == node.key)
                new_node.neighbors.append(new_neighbor)

        new_graph = Graph([], [])
        new_graph.nodes = new_nodes

        return new_graph

    def reduced(self):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search()

        flipped_graph = self.flip_edges()

        for node in flipped_graph.nodes:
            node.key = finish_numbers[node.key]

        flipped_graph.reduce_to_tree(decreasing=True)

        visited = {}
        for node in flipped_graph.nodes:
            visited[node.key] = False

        def dfs(node, keys):
            nonlocal visited
            for neighbor in node.neighbors:
                if not visited[neighbor.key]:
                    visited[neighbor.key] = True
                    keys.append(neighbor.value)
                    dfs(neighbor, keys)

        new_nodes = []
        for index, node in enumerate(flipped_graph.nodes):
            if not visited[node.key]:
                visited[node.key] = True
                keys = []
                keys.append(node.value)
                dfs(node, keys)
                new_node = GraphNode(index, keys)
                new_node.value = keys
                new_nodes.append(new_node)

        for new_node in new_nodes:
            for key in new_node.value:
                original_node = next(x for x in self.nodes if x.key == key)
                for neighbor in original_node.neighbors:
                    new_neighbor = next((x for x in new_nodes if neighbor.key in x.value))
                    if not new_node == new_neighbor and not new_neighbor in new_node.neighbors:
                        new_node.neighbors.append(new_neighbor)

        for node in new_nodes:
            node.value = ",".join(map(str, node.value))

        reduced_graph = Graph([], [])
        reduced_graph.nodes = new_nodes

        return reduced_graph

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


def get_edgesets_dfs(data, iterations, tree_edges, back_edges):
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
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
        depth_numbers, finish_numbers, current_tree_edges, current_back_edges, forward_edges, cross_edges = graph.depth_first_search()

        if len(current_tree_edges) == tree_edges and 1 <= len(current_back_edges) == back_edges:
            if adj_matrix not in edgesets:
                edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def get_edgesets_reduction(edges, iterations, groups):
    keys = [1, 2, 3, 4, 5]
    edgesets = []

    for iteration in range(iterations):
        adj_matrix = [[0 for y in range(5)] for x in range(5)]
        for edge in range(edges):
            while True:
                i, j = random.randint(0, 4), random.randint(0, 3)
                if j >= i:
                    j += 1
                if adj_matrix[j][i] == 0:
                    adj_matrix[i][j] = 1
                    break

        empty = False
        for i in range(len(adj_matrix)):
            row_empty = True
            for j in range(len(adj_matrix[i])):
                if adj_matrix[i][j] == 1:
                    row_empty = False
                    break
            if row_empty:
                empty = True
                break

        if empty:
            continue

        graph = Graph(adj_matrix, keys)
        reduced_graph = graph.reduced()
        if len(reduced_graph.nodes) == groups:
            if adj_matrix not in edgesets:
                edgesets.append(copy.deepcopy(adj_matrix))

    return edgesets


def make_question_dfs(dataset, seed):
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(12)] for x in range(12)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 12 + j]

    graph = Graph(adj_matrix, keys)
    depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = graph.depth_first_search()

    back_edges = back_edges + ([""] * (3 - len(back_edges)))
    forward_edges = forward_edges + ([""] * (3 - len(forward_edges)))
    cross_edges = cross_edges + ([""] * (3 - len(cross_edges)))

    answer_graph = copy.deepcopy(graph)
    for node in answer_graph.nodes:
        node.value = f"${node.value}^{{{depth_numbers[node.key]},{finish_numbers[node.key]}}}$"

    dag = copy.deepcopy(graph)
    dag.reduce_to_dag()
    topological_order = dag.topological_order()
    topological_order_string = " & ".join(map(str, topological_order))

    question_string = f"""
    \\item{{
            Járjuk be az 1-es csúcsból indulva \\textbf{{mélységi bejárással}} az alábbi gráfot!
            A csúcsok szomszédjainak feldolgozási sorrendje legyen a csúcsok címkéiben nagyság szerint növekedően rendezett.
            Jelöljük a gráfon a bejárás során a csúcsokhoz rendelt mélységi és befejezési számokat, és ezek alapján osztályozzuk a gráf éleit!
            Írja be a talált  \\textbf{{nem faéleket}} a táblázatba (pl. 3 → 7)!\\\\[1em]
            {graph.print_in_latex()}
            \\hfill
            \\begin{{tabular}}{{ |c|c|c| }}
            \\hline
            Visszaélek & Előreélek & Keresztélek \\\\
            \\hline
            & & \\\\
            & & \\\\
            & & \\\\
            \\hline
            \\end{{tabular}}
    }}   
    \\item{{
        Állapítsuk meg, hogy az előző feladatban szereplő gráf \\textbf{{DAG}} tulajdonságú-e! 
        Ha nem az, a mélységi bejárás eredménye alapján a lehető legkevesebb él törlésével alakítsuk \\textbf{{DAG}} tulajdonságúvá
        , és adjuk meg a csúcsok egy topologikus rendezését!\\
        \\begin{{center}}
        \\begin{{tabular}}{{| m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} |}}
            \\hline
            & & & & & & & & & & & \\\\
            & & & & & & & & & & & \\\\
            \\hline
        \\end{{tabular}}
        \\end{{center}}
    }}     
    """

    answer_string = f"""
    \\item{{
            Járjuk be az 1-es csúcsból indulva \\textbf{{mélységi bejárással}} az alábbi gráfot!
            A csúcsok szomszédjainak feldolgozási sorrendje legyen a csúcsok címkéiben nagyság szerint növekedően rendezett.
            Jelöljük a gráfon a bejárás során a csúcsokhoz rendelt mélységi és befejezési számokat, és ezek alapján osztályozzuk a gráf éleit!
            Írja be a talált  \\textbf{{nem faéleket}} a táblázatba (pl. 3 → 7)!\\\\[1em]
            {answer_graph.print_in_latex()}
            \\hfill
            \\begin{{tabular}}{{ |c|c|c| }}
            \\hline
            Visszaélek & Előreélek & Keresztélek \\\\
            \\hline
            {back_edges[0]} & {forward_edges[0]} & {cross_edges[0]} \\\\
            {back_edges[1]} & {forward_edges[1]} & {cross_edges[1]} \\\\
            {back_edges[2]} & {forward_edges[2]} & {cross_edges[2]} \\\\
            \\hline
            \\end{{tabular}}
    }}
    \\item{{
        Állapítsuk meg, hogy az előző feladatban szereplő gráf \\textbf{{DAG}} tulajdonságú-e! 
        Ha nem az, a mélységi bejárás eredménye alapján a lehető legkevesebb él törlésével alakítsuk \\textbf{{DAG}} tulajdonságúvá
        , és adjuk meg a csúcsok egy topologikus rendezését!\\
        \\begin{{center}}
        \\begin{{tabular}}{{| m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} | m{{2em}} |}}
            \\hline
            {topological_order_string} \\\\
            & & & & & & & & & & & \\\\
            \\hline
        \\end{{tabular}}
        \\end{{center}}
    }}     
    """

    back_edges_string = ""
    for edge in back_edges:
        if edge == "":
            continue
        back_edges_string += f"{edge[0]}→{edge[1]},"
    back_edges_string = back_edges_string[:-1]

    forward_edges_string = ""
    for edge in forward_edges:
        if edge == "":
            continue
        forward_edges_string += f"{edge[0]}→{edge[1]},"
    forward_edges_string = forward_edges_string[:-1]

    cross_edges_string = ""
    for edge in cross_edges:
        if edge == "":
            continue
        cross_edges_string += f"{edge[0]}→{edge[1]},"
    cross_edges_string = cross_edges_string[:-1]

    answer = [back_edges_string, forward_edges_string, cross_edges_string, " ".join(map(str, topological_order))]

    return question_string, answer_string, answer


def make_question_reduction(dataset, seed):
    keys = [1, 2, 3, 4, 5]
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(5)] for x in range(5)]

    matrix_string = ""
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 5 + j]
        matrix_string += "\t\t" + " & ".join(map(str, adj_matrix[i])) + "\\\\\n"

    graph = Graph(adj_matrix, keys)
    reduced_graph = graph.reduced()

    question_string = f"""
    \\item{{
        Határozzuk meg az alábbi, szomszédsági mátrixszal megadott gráf \\textbf{{redukált gráfját}}!\\\\[1em]
        \\begin{{center}}
        $\\begin{{pmatrix}}
{matrix_string[:-3]}
        \\end{{pmatrix}}$
        \\vspace*{{-2in}}
        \\end{{center}}
    }}
    """

    answer_string = f"""
    \\item{{
        Határozzuk meg az alábbi, szomszédsági mátrixszal megadott gráf \\textbf{{redukált gráfját}}!\\\\[1em]
        \\begin{{center}}
        {reduced_graph.print_in_latex()}
        \\vspace*{{-2in}}
        \\end{{center}}
    }}
    """

    return question_string, answer_string, [reduced_graph.print_edges()]
