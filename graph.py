class GraphNode:
    def __init__(self, key):
        self.key = key
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

    def reduce_to_dag(self):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search()
        for node in self.nodes:
            node.neighbors = [neighbor for neighbor in node.neighbors if not (node.key, neighbor.key) in back_edges]

    def topological_order(self):
        depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = self.depth_first_search()
        node_keys = [node.key for node in self.nodes]
        node_keys.sort(key=lambda key: finish_numbers[key], reverse=True)
        return node_keys

    def print_in_latex(self):
        print("\\begin{tikzpicture}[>=Latex]")
        print("\\graph[simpleer, spring layout]{")

        edges_string = ""
        for node in self.nodes:
            for neighbor in node.neighbors:
                edges_string += f"{node.key} -> {neighbor.key}, "

        print(edges_string)

        print("};\n\\end{tikzpicture}")
