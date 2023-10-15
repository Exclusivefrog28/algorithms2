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
        print("\\begin{tikzpicture}[>=Latex]")
        print("\\graph[simpleer, spring layout]{")

        edges_string = ""
        for node in self.nodes:
            for neighbor in node.neighbors:
                edges_string += f"\"{node.value}\" -> \"{neighbor.value}\", "

        print(edges_string)

        print("};\n\\end{tikzpicture}")
        print("\\\\")
