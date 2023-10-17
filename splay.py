import random


class SplayTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None
        self.single_rotations = 0
        self.double_rotations = 0

    def insert(self, key):
        current_node = self.root

        if current_node is None:
            self.root = SplayTreeNode(key)
            return

        while True:
            if key < current_node.key:
                if current_node.left is None:
                    current_node.left = SplayTreeNode(key)
                    current_node.left.parent = current_node
                    self.splay(current_node.left)
                    return
                else:
                    current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = SplayTreeNode(key)
                    current_node.right.parent = current_node
                    self.splay(current_node.right)
                    return
                else:
                    current_node = current_node.right

    def splay(self, node):
        if node.parent is None:
            return

        parent = node.parent
        grandparent = parent.parent

        if grandparent is None:
            self.single_rotations += 1
            if node == parent.left:
                self.right_rotate(parent)
            else:
                self.left_rotate(parent)
        else:
            self.double_rotations += 1

            if node == parent.left and parent == grandparent.left:
                self.right_rotate(grandparent)
                self.right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                self.left_rotate(grandparent)
                self.left_rotate(parent)
            elif node == parent.left and parent == grandparent.right:
                self.right_rotate(parent)
                self.left_rotate(grandparent)
            elif node == parent.right and parent == grandparent.left:
                self.left_rotate(parent)
                self.right_rotate(grandparent)

        self.splay(node)

    def right_rotate(self, node):
        new_root = node.left
        new_root.parent = node.parent

        if new_root.parent is not None:
            if new_root.parent.left == node:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root
        else:
            self.root = new_root

        node.parent = new_root
        node.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = node
        new_root.right = node

    def left_rotate(self, node):
        new_root = node.right
        new_root.parent = node.parent

        if new_root.parent is not None:
            if new_root.parent.left == node:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root
        else:
            self.root = new_root

        node.parent = new_root
        node.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = node
        new_root.left = node

    def print_in_latex(self, obscure=None):

        tree_string = f"""
        \\begin{{tikzpicture}}[level/.style={{sibling distance=80mm/#1}},scale=0.7,transform shape]
        \\{self._print_in_latex_helper(self.root, obscure)};
        \\end{{tikzpicture}}
        """

        return tree_string

    def _print_in_latex_helper(self, node, obscure):

        if node is None:
            return ""

        left_child = f"child {{{self._print_in_latex_helper(node.left, obscure)}}}" if node.left is not None else "child[missing]"
        right_child = f"child {{{self._print_in_latex_helper(node.right, obscure)}}}" if node.right is not None else "child[missing]"

        if node.left is None and node.right is None:
            left_child, right_child = "", ""

        key = node.key
        if obscure is not None:
            if node.key == obscure[0]:
                key = "X"
            elif node.key == obscure[1]:
                key = "Y"
            elif node.key == obscure[2]:
                key = "Z"
            else:
                key = "?"

        return f"node [circle,draw] {{{key}}} {left_child} {right_child}"

def get_permutations(data, iterations, single_rotations, double_rotations):
    selected_permutations = []

    for i in range(iterations):
        tree = SplayTree()
        random.shuffle(data)
        for x in data:
            tree.insert(x)
        if tree.single_rotations == single_rotations and tree.double_rotations == double_rotations:
            if data not in selected_permutations:
                selected_permutations.append(data.copy())

    return selected_permutations


def make_question(dataset, seed):
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))
    tree = SplayTree()
    for x in data:
        tree.insert(x)

    data_string = ", ".join(map(str, data))

    obscure = random.sample(data[0:-1], 3)

    question_string = f"""
    \\item{{
        Építsünk \\textbf{{S-fát}} a következő adatokból: 
        \\textbf{{{data_string}}} !\\\\[1em]
        A fa végső állapotában milyen kulcsok találhatóak az X,Y,Z helyeken?\\\\[1em]
        \\begin{{center}}
        {tree.print_in_latex(obscure)}
        \\end{{center}}
    }}
    """
    answer_string = f"""
    \\item{{
        Építsünk \\textbf{{S-fát}} a következő adatokból: 
        \\textbf{{{data_string}}} !\\\\[1em]
        A fa végső állapotában milyen kulcsok találhatóak az X,Y,Z helyeken?\\\\
        X: {obscure[0]}, Y: {obscure[1]}, Z: {obscure[2]}\\\\
        \\begin{{center}}
        {tree.print_in_latex()}
        \\end{{center}}
    }}
    """

    return question_string, answer_string
