import copy
import random
import sys

from avl import AVLTree
from bplus import BPlusTree
from graph import Graph
from splay import SplayTree

seed = sys.argv[1]
question = sys.argv[2]

print("""\\documentclass{article}
    \\usepackage[a4paper, margin=0.7in]{geometry}
    \\usepackage{tikz}
    \\usepackage{array}
    \\usepackage{amsmath}
    \\usetikzlibrary{trees, arrows.meta,}
    \\usetikzlibrary{graphs,graphdrawing,trees,arrows.meta,shapes.multipart}
    \\tikzset{graphs/simpleer/.style={nodes={draw, circle},node distance=1.75cm, nodes={minimum size=2em}}}
    \\usegdlibrary{circular,force,layered,routing}
    \\usepackage{forest}
    \\newcommand\\mpnc[3]{\\nodepart{one} $#1$\\nodepart{two} $#2$\\nodepart{three} $#3$}
    \\begin{document}
    """)

random.seed(seed)

if question == '1a':
    with open("avl_3s_0d.txt", "r") as f:
        dataset = f.readlines()
        f.close()
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))

    tree = AVLTree()

    prev_single_rots, prev_double_rots = 0, 0

    for x in data:
        tree.insert(x)

        rotation_string = ""
        if prev_single_rots != tree.right_rotations:
            if prev_double_rots != tree.left_rotations:
                rotation_string = "- kettős forgatás"
            else:
                rotation_string = "- jobbra forgatás"
        elif prev_double_rots != tree.left_rotations:
            rotation_string = "- balra forgatás"

        prev_single_rots = tree.right_rotations
        prev_double_rots = tree.left_rotations
        print("\\vspace{0.5cm}")
        print(f"{x} beszúrása {rotation_string}\\\\")
        print(tree.print_in_latex())

elif question == "1b":
    with open("avl_1s_1d.txt", "r") as f:
        dataset = f.readlines()
        f.close()
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))

    tree = AVLTree()

    prev_single_rots, prev_double_rots = 0, 0

    for x in data:
        tree.insert(x)

        rotation_string = ""
        if prev_single_rots != tree.right_rotations:
            if prev_double_rots != tree.left_rotations:
                rotation_string = "- kettős forgatás"
            else:
                rotation_string = "- jobbra forgatás"
        elif prev_double_rots != tree.left_rotations:
            rotation_string = "- balra forgatás"

        prev_single_rots = tree.right_rotations
        prev_double_rots = tree.left_rotations
        print("\\vspace{0.5cm}")
        print(f"{x} beszúrása {rotation_string}\\\\")
        print(tree.print_in_latex())

elif question == "2":
    with open("bplus.txt", "r") as f:
        dataset = f.readlines()
        f.close()
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))
    inserts = data[0:-4]
    deletions = data[-4:]

    tree = BPlusTree(4)
    prev_splits = 0
    for x in inserts:
        tree.insert(x)
        print("\\vspace{0.5cm}")
        print(f"{x} beszúrása {'- szétválasztás' if prev_splits != tree.splits else ''}\\\\")
        print(tree.print_in_latex())
        prev_splits = tree.splits

    prev_rebal_l, prev_rebal_nl = 0, 0
    prev_merge_l, prev_merge_nl = 0, 0

    for x in deletions:
        tree.delete(x)
        action = ""
        if prev_rebal_l != tree.rebalances_leaf:
            action += "- elosztás levélben "
        if prev_rebal_nl != tree.rebalances_non_leaf:
            action += "- elosztás nem levélben "
        if prev_merge_l != tree.merges_leaf:
            action += "- egyesítés levélben "
        if prev_merge_nl != tree.merges_non_leaf:
            action += "- egyesítés nem levélben "

        print("\\vspace{0.5cm}")
        print(f"{x} törlése {action}\\\\")
        print(tree.print_in_latex())
        prev_rebal_l = tree.rebalances_leaf
        prev_rebal_nl = tree.rebalances_non_leaf
        prev_merge_l = tree.merges_leaf
        prev_merge_nl = tree.merges_non_leaf

elif question == "3":
    with open("splay.txt", "r") as f:
        dataset = f.readlines()
        f.close()

    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))
    tree = SplayTree()

    prev_single_rots, prev_double_rots = 0, 0

    for x in data:
        tree.insert(x)

        rotation_string = ""
        if prev_single_rots != tree.single_rotations:
            rotation_string += f"- {tree.single_rotations - prev_single_rots} egyszeres forgatás"
        if prev_double_rots != tree.double_rotations:
            rotation_string += f"- {tree.double_rotations - prev_double_rots} kettős forgatás"

        prev_single_rots = tree.single_rotations
        prev_double_rots = tree.double_rotations
        print("\\vspace{0.5cm}")
        print(f"{x} beszúrása {rotation_string}\\\\")
        print(tree.print_in_latex())

elif question == "4" or question == "5":
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    with open("dfs.txt", "r") as f:
        dataset = f.readlines()
        f.close()
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(12)] for x in range(12)]

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 12 + j]

    graph = Graph(adj_matrix, keys)

    depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = graph.depth_first_search()

    answer_graph = copy.deepcopy(graph)
    for node in answer_graph.nodes:
        node.value = f"${node.value}^{{{depth_numbers[node.key]},{finish_numbers[node.key]}}}$"

    print(answer_graph.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    dag = copy.deepcopy(graph)
    dag.reduce_to_dag()
    depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = dag.depth_first_search()
    for node in dag.nodes:
        node.value = f"${node.value}^{{{depth_numbers[node.key]},{finish_numbers[node.key]}}}$"

    print(dag.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    topological_order = dag.topological_order()
    topological_order_string = " ".join(map(str, topological_order))
    print(topological_order_string)

elif question == "6":
    keys = [1, 2, 3, 4, 5]
    with open("reduction.txt", "r") as f:
        dataset = f.readlines()
        f.close()
    data = dataset[random.randint(0, len(dataset) - 1)]
    data = list(map(int, data[:-1].split(" ")))
    adj_matrix = [[0 for y in range(5)] for x in range(5)]
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            adj_matrix[i][j] = data[i * 5 + j]

    graph = Graph(adj_matrix, keys)
    print(graph.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    answer_graph = copy.deepcopy(graph)

    depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = answer_graph.depth_first_search()
    for node in answer_graph.nodes:
        node.value = f"${node.value}^{{{depth_numbers[node.key]},{finish_numbers[node.key]}}}$"

    print(answer_graph.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    flipped_graph = graph.flip_edges()

    for node in flipped_graph.nodes:
        node.key = finish_numbers[node.key]

    print(flipped_graph.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    answer_graph = copy.deepcopy(flipped_graph)

    depth_numbers, finish_numbers, tree_edges, back_edges, forward_edges, cross_edges = answer_graph.depth_first_search(decreasing_order=True)
    for node in answer_graph.nodes:
        node.value = f"${node.value}^{{{depth_numbers[node.key]},{finish_numbers[node.key]}}}$"

    print(answer_graph.print_in_latex())
    print("\\\\")
    print("\\vspace{0.5cm}")

    reduced_graph = graph.reduced()
    print(reduced_graph.print_in_latex())


print("\\end{document}")
