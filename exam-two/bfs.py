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

        for node in self.nodes:
            d[node.key] = "∞"
            pi[node.key] = None

        def print_step(queue, visited, d, pi):
            queue_keys = []
            for node in queue:
                queue_keys.append(node.key)

            print(f"{' '.join(map(str, queue_keys))} & {' '.join(map(str, visited))} & {' & '.join(map(str, d.values()))} & {' & '.join(map(str, pi.values()))}\\\\")
            print('\\hline')


        def bfs(node):
            visited.append(node.key)
            queue.append(node)
            d[node.key] = 0
            print_step(queue, visited, d, pi)
            while not len(queue) == 0:
                current_node = queue.pop(0)
                for neighbor in current_node.neighbors:
                    if neighbor.key not in visited:
                        visited.append(neighbor.key)
                        queue.append(neighbor)
                        d[neighbor.key] = d[current_node.key] + 1
                        pi[neighbor.key] = current_node.key

                print_step(queue, visited, d, pi)

        for node in self.nodes:
            if node.key not in visited:
                bfs(node)

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
