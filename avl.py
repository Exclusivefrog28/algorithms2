import random


class AVLTreeNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value if value else key
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.balance = 0


class AVLTree:
    def __init__(self):
        self.root = None
        self.single_rotations = 0
        self.double_rotations = 0
        self.right_rotations = 0
        self.left_rotations = 0
        self.tipping_inserts = []

    def insert(self, key, value=None):
        if self.root is None:
            self.root = AVLTreeNode(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = AVLTreeNode(key, value)
                node.left.parent = node
                self.rebalance(node, key)
            else:
                self._insert(node.left, key, value)

        else:
            if node.right is None:
                node.right = AVLTreeNode(key, value)
                node.right.parent = node
                self.rebalance(node, key)
            else:
                self._insert(node.right, key, value)

    def rebalance(self, node, key):
        self.calculate_heights(node)

        if node.balance == 2:
            self.tipping_inserts.append(key)
            if node.right.balance == -1:
                self.right_rotate(node.right)
                self.double_rotations += 1
            else:
                self.single_rotations += 1
            self.left_rotate(node)
        elif node.balance == -2:
            self.tipping_inserts.append(key)
            if node.left.balance == 1:
                self.left_rotate(node.left)
                self.double_rotations += 1
            else:
                self.single_rotations += 1
            self.right_rotate(node)
        elif node.parent is not None:
            self.rebalance(node.parent, key)

    def right_rotate(self, node):
        self.right_rotations += 1

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

        self.calculate_heights(new_root.right)
        self.calculate_heights(new_root)

    def left_rotate(self, node):
        self.left_rotations += 1

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

        self.calculate_heights(new_root.left)
        self.calculate_heights(new_root)

    def calculate_heights(self, node):
        left_height = node.left.height if node.left is not None else 0
        right_height = node.right.height if node.right is not None else 0
        node.height = 1 + max(left_height, right_height)
        node.balance = right_height - left_height

    def print_in_latex(self):
        tree_string = "\\begin{tikzpicture}[level/.style={sibling distance=64mm/#1},scale=0.7,transform shape]\n"
        tree_string += "\\" + self._print_in_latex_helper(self.root) + ";"
        tree_string += "\\end{tikzpicture}\n"

        return tree_string

    def _print_in_latex_helper(self, node):
        if node is None:
            return ""

        left_child = f"child {{{self._print_in_latex_helper(node.left)}}}" if node.left is not None else "child[missing]"
        right_child = f"child {{{self._print_in_latex_helper(node.right)}}}" if node.right is not None else "child[missing]"

        if node.left is None and node.right is None:
            left_child, right_child = "", ""

        return f"node [circle,draw] {{{node.value}}} {left_child} {right_child}"


def get_permutations(data, iterations, single_rotations, double_rotations):
    selected_permutations = []

    for i in range(iterations):
        tree = AVLTree()
        random.shuffle(data)
        for x in data:
            tree.insert(x)
        if tree.single_rotations == single_rotations and tree.double_rotations == double_rotations:
            if data not in selected_permutations:
                selected_permutations.append(data.copy())

    return selected_permutations


def print_dependencies():
    print("\\usepackage{tikz}")


def make_question(dataset, seed):
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))
    correct_tree = AVLTree()
    for x in data:
        correct_tree.insert(x)

    data_string = ", ".join(map(str, data))

    question_keys = random.sample(data, 3)
    question_data = [
        "?" if x not in question_keys else "X" if x == question_keys[0] else "Y" if x == question_keys[1] else "Z" for x
        in data]

    question_tree = AVLTree()
    for i in range(len(question_data)):
        question_tree.insert(data[i], question_data[i])

    question_string = f"""
        \\item {{Adatok: \\textbf{{{data_string}}}
        \\begin{{enumerate}}
            \\item {{Hány jobbra forgatás volt szükséges a beszúrások során?}}\\\\[1em]
            \\item {{Mely kulcsok beszúrásakor sérül az AVL tulajdonság (hogy azt egy forgatással helyre kell állítani)?}}\\\\[1em]
            \\item {{
                A fa végső állapotában melyik kulcsok találhatók az X, Y, és Z-vel jelölt csúcsokban?\\\\
                \\begin{{center}}
                {question_tree.print_in_latex()}\\\\[2em]
                \\end{{center}}
            }}
        \\end{{enumerate}}}}
        """

    answer_string = f"""
        \\item {{Adatok: \\textbf{{{data_string}}}
        \\begin{{enumerate}}
            \\item {{Hány jobbra forgatás volt szükséges a beszúrások során?\\\\{correct_tree.right_rotations}}}\\\\
            \\item {{Mely kulcsok beszúrásakor sérül az AVL tulajdonság (hogy azt egy forgatással helyre kell állítani)?\\\\{",".join(map(str, correct_tree.tipping_inserts))}}}\\\\
            \\item {{A fa végső állapotában melyik kulcsok találhatók az X, Y, és Z-vel jelölt csúcsokban?\\\\X={question_keys[0]}, Y={question_keys[1]}, Z={question_keys[2]}}}\\\\\
            \\begin{{center}}
            {correct_tree.print_in_latex()}\\\\[2em]
            \\end{{center}}
            }}
            \\end{{enumerate}}}}
    """

    return question_string, answer_string
