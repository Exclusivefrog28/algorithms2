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


class UndirectedGraph:
    def __init__(self, adj_matrix, keys):
        self.nodes = []
        for i, row in enumerate(adj_matrix):
            self.nodes.append(GraphNode(keys[i]) if keys else GraphNode(i))
        for i, row in enumerate(adj_matrix):
            for j, value in enumerate(row):
                if value != 0:
                    self.nodes[i].neighbors.append((self.nodes[j], value))
                    self.nodes[j].neighbors.append((self.nodes[i], value))

    def print_in_latex(self, color=None):
        graph_string = f"""\\begin{{tikzpicture}}[>=Latex]
            \\graph[simpleer, spring layout, orient=right, edge quotes mid, edges={{nodes={{fill=white, inner sep=1pt}}}} {
        ', node distance=2.75cm, nodes={minimum size=2.5em}' if len(self.nodes) > 6 else ''}]{{
            {self.print_edges(color)}
            }};
            \\end{{tikzpicture}}"""

        return graph_string

    def print_edges(self, color=None):
        edges_string = ""
        for node in self.nodes:
            for neighbor in node.neighbors:
                if neighbor[0].key < node.key:
                    continue
                colored = color and ((node.key, neighbor[0].key) in color or (neighbor[0].key, node.key) in color)
                weight = f"[\"{neighbor[1]}\"{',color=blue' if colored else ''}]"
                edges_string += f"\"{node.value}\" --{weight} \"{neighbor[0].value}\", "
        return edges_string
