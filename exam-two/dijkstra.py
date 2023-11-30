import copy

from weighted_graph import Graph

def dijkstra(graph, start):
    result = []

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
                distances[neighbor[0].key] = temp_distance
                previous_nodes[neighbor[0]] = current_node
                temp = unvisited_nodes[0]
                unvisited_nodes[0] = unvisited_nodes[unvisited_nodes.index(neighbor[0])]
                unvisited_nodes[unvisited_nodes.index(neighbor[0])] = temp

        result.append((visited_nodes.copy(), distances.copy().values(), previous_nodes.copy().values()))

    return result


def print_table(steps):
    table = """\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}
        \\hline
        \\multirow{2}{*}{KÉSZ} & \\multicolumn{6}{c|}{d} & \\multicolumn{6}{c|}{\\Pi}\\\\
        \\cline{2-13}
        & 1 & 2 & 3 & 4 & 5 & 6 & 1 & 2 & 3 & 4 & 5 & 6\\\\
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
