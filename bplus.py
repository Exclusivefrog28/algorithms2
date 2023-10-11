import math


class BPlusNode:
    def __init__(self, leaf, degree):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.degree = degree
        for i in range(degree):
            self.children.append(None)

    def append_key(self, key, right_child=None):
        self.keys.append(key)
        if len(self.keys) >= len(self.children):
            self.children.append(right_child)
        else:
            self.children[len(self.keys)] = right_child

        for i in range(len(self.keys) - 1, -1, -1):
            if key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                self.children[i + 2] = self.children[i + 1]
                self.keys[i] = key
                self.children[i + 1] = right_child

    def split(self, key, right_child=None):
        self.append_key(key, right_child)

        right = BPlusNode(self.leaf, self.degree)
        right.children.append(None)

        for i in range(math.ceil(len(self.keys) / 2), len(self.keys)):
            right.keys.append(self.keys[i])
            right.children.append(self.children[i + 1])

        self.keys = self.keys[0: math.ceil(len(self.keys) / 2)]
        self.children = self.children[0: math.ceil(len(self.children) / 2) + 1]

        return right.keys[0], right


def search(keys, key):
    for i in range(len(keys)):
        if keys[i] >= key:
            return i
    return len(keys)


class BPlusTree:
    def __init__(self, degree=4):
        self.root = BPlusNode(True, degree - 1)
        self.degree = degree - 1

    def insert(self, key):

        if len(self.root.keys) == 0:
            self.root.keys.append(key)
            return

        split_key, right = self._insert(self.root, key)

        if split_key is not None:
            new_root = BPlusNode(False, self.degree)
            new_root.keys.append(split_key)
            new_root.children[0] = self.root
            new_root.children[1] = right
            self.root = new_root

    def _insert(self, node, key):
        if node.leaf:
            if len(node.keys) > self.degree - 1:
                split_key, right = node.split(key)

                return split_key, right
            else:
                node.append_key(key)
            return None, None

        index = search(node.keys, key)

        insertion_point = node.children[index]

        if insertion_point is None:
            insertion_point = BPlusNode(True, self.degree)
            node.children[index] = insertion_point

        split_key, right = self._insert(insertion_point, key)

        if split_key is not None:
            if len(node.keys) > self.degree - 1:
                split_key, right = node.split(split_key, right)

                return split_key, right
            else:
                node.append_key(split_key, right)
                return None, None

        return None, None

    def print_in_latex(self):
        print("\\begin{forest}")
        print(
            f"for tree = {{rectangle split, rectangle split horizontal, rectangle split parts={self.degree}, draw, parent anchor=south, child anchor=north, edge = {{-Stealth, semithick, shorten >= 1mm, shorten <= 1mm}}, l sep=12mm, s sep=1mm}}")
        print(self._print_in_latex(self.root))
        print(f"\\end{{forest}}")
        print(f"\\\[20pt]")

    def _print_in_latex(self, node):

        if node is None:
            return ""

        keys = node.keys.copy()
        children = node.children if not node.leaf else []

        while len(keys) < self.degree:
            keys.append("")

        latex_string = "[{\\mpnc"
        for i in range(len(keys)):
            latex_string += f"{{{keys[i]}}}"
        latex_string += "}"
        for i in range(len(children)):
            if children[i] is None:
                continue
            latex_string += "\n"
            latex_string += self._print_in_latex(children[i])
        latex_string += "\n]"

        return latex_string
