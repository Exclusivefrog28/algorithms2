import copy
import math
import random


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

    def remove_key(self, index):
        self.keys = self.keys[0: index] + self.keys[index + 1:]
        self.children = self.children[:index + 1] + self.children[index + 2:]

    def split(self, key, right_child=None):
        self.append_key(key, right_child)

        right = BPlusNode(self.leaf, self.degree)
        split_key = self.keys[math.ceil(len(self.keys) / 2)]

        if self.leaf:
            right.keys = self.keys[math.ceil(len(self.keys) / 2):]
        else:
            right.keys = self.keys[math.ceil(len(self.keys) / 2) + 1:]
            right.children = self.children[math.ceil(len(self.keys) / 2) + 1:]

        self.keys = self.keys[0: math.ceil(len(self.keys) / 2)]
        self.children = self.children[0: math.ceil(len(self.children) / 2)]

        return split_key, right

    def merge(self, other_node):
        if self.keys[0] < other_node.keys[0]:
            self.keys = self.keys + other_node.keys
            self.children = self.children + other_node.children[1:]
        else:
            self.keys = other_node.keys + self.keys
            self.children = other_node.children + self.children[1:]


def search(keys, key):
    for i in range(len(keys)):
        if keys[i] > key:
            return i
    return len(keys)


class BPlusTree:
    def __init__(self, degree=4):
        self.root = BPlusNode(True, degree - 1)
        self.degree = degree - 1
        self.splits = 0
        self.rebalances_leaf = 0
        self.merges_leaf = 0
        self.rebalances_non_leaf = 0
        self.merges_non_leaf = 0

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
                self.splits += 1
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
                self.splits += 1
                return split_key, right
            else:
                node.append_key(split_key, right)
                return None, None

        return None, None

    def delete(self, key):
        self._delete(self.root, key)
        if len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        if node.leaf:
            if key in node.keys:
                node.keys.remove(key)
                if len(node.keys) == 0:
                    if node == self.root:
                        self.root = BPlusNode(True, self.degree)
                    else:
                        node = None
                elif len(node.keys) < (self.degree + 1) // 2:
                    return True

            return False

        index = search(node.keys, key)
        child = node.children[index]
        if child is not None:
            if self._delete(child, key):
                target_sibling = None
                target_right = False
                if index > 0:
                    left = node.children[index - 1]
                    if (left is not None and (len(left.keys) > (self.degree + 1) // 2)
                            or (not child.leaf and (len(left.keys) + 1 > (self.degree + 1) // 2))):
                        target_sibling = left
                if index < len(node.keys) and target_sibling is None:
                    right = node.children[index + 1]
                    if (right is not None and (len(right.keys) > (self.degree + 1) // 2)
                            or (not child.leaf and (len(right.keys) + 1 > (self.degree + 1) // 2))):
                        target_sibling = right
                        target_right = True

                if target_sibling is not None:
                    if child.leaf:
                        self.rebalances_leaf += 1
                        if target_right:
                            child.append_key(target_sibling.keys[0], target_sibling.children[1])
                            target_sibling.remove_key(0)
                            new_split_key = target_sibling.keys[0]
                            node.keys[index] = new_split_key
                        else:
                            child.append_key(target_sibling.keys[-1], target_sibling.children[len(target_sibling.keys)])
                            target_sibling.remove_key(len(target_sibling.keys) - 1)
                            new_split_key = child.keys[0]
                            node.keys[index - 1] = new_split_key
                    else:
                        self.rebalances_non_leaf += 1
                        if target_right:
                            child.children.append(target_sibling.children[0])
                            target_sibling.children = target_sibling.children[1:]
                            child.keys.append(node.keys[index - 1])
                            node.keys[index - 1] = target_sibling.keys[0]
                            target_sibling.keys = target_sibling.keys[1:]
                        else:
                            child.children.append(child.children[0])
                            child.children[0] = target_sibling.children[-1]
                            target_sibling.children = target_sibling.children[:-1]
                            child.keys.append(node.keys[index - 1])
                            node.keys[index - 1] = target_sibling.keys[-1]
                            target_sibling.keys = target_sibling.keys[:-1]

                else:
                    if child.leaf:
                        self.merges_leaf += 1
                        if index > 0:
                            node.children[index - 1].merge(child)
                            node.remove_key(index - 1)
                        else:
                            child.merge(node.children[index + 1])
                            node.remove_key(0)
                    else:
                        self.merges_non_leaf += 1
                        if index > 0:
                            target_sibling = node.children[index - 1]
                            target_sibling.children.append(child.children[0])
                            target_sibling.keys.append(node.keys[index - 1])
                            node.remove_key(index - 1)
                        else:
                            target_sibling = node.children[index + 1]
                            child.children = [child.children[0]] + target_sibling.children
                            child.keys = [node.keys[0]] + target_sibling.keys
                            node.remove_key(0)

                    if len(node.keys) == 0:
                        return True
        else:
            return False

    def print_in_latex(self, obscure=None):
        string = f"""
            \\begin{{forest}}
            for tree = {{rectangle split, rectangle split horizontal, rectangle split parts={self.degree}, draw, parent anchor = south, child anchor = north, 
            edge = {{-Stealth, semithick, shorten >= 1mm, shorten <= 1mm}}, l sep = 12mm, s sep = 1mm}}
            {self._print_in_latex(self.root, obscure)}
            \\end{{forest}}
        """

        return string

    def _print_in_latex(self, node, obscure):

        if node is None:
            return ""

        keys = node.keys.copy()
        children = node.children if not node.leaf else []

        while len(keys) < self.degree:
            keys.append("")

        latex_string = "[{\\mpnc"
        for i in range(len(keys)):
            if obscure is not None:
                if keys[i] == obscure[0]:
                    latex_string += "{X}"
                elif keys[i] == obscure[1]:
                    latex_string += "{Y}"
                elif keys[i] == obscure[2]:
                    latex_string += "{Z}"
                else:
                    latex_string += "{}"
            else:
                latex_string += f"{{{keys[i]}}}"
        latex_string += "}"
        for i in range(len(children)):
            if children[i] is None:
                continue
            latex_string += self._print_in_latex(children[i], obscure)
        latex_string += "]"

        return latex_string


def get_permutations(data, iterations, splits, leaf_rebalances, inner_rebalances, leaf_merges, inner_merges):
    selected_permutations = []

    for i in range(iterations):
        tree = BPlusTree()
        random.shuffle(data)
        current_data = data.copy()
        for x in current_data:
            tree.insert(x)
        if tree.splits == splits:
            if current_data not in selected_permutations:
                while True:
                    new_tree = copy.deepcopy(tree)
                    deletions = random.sample(current_data, 4)
                    for x in deletions:
                        new_tree.delete(x)
                    if (new_tree.rebalances_leaf == leaf_rebalances and
                            new_tree.rebalances_non_leaf == inner_rebalances and
                            new_tree.merges_leaf == leaf_merges and
                            new_tree.merges_non_leaf == inner_merges):
                        current_data += deletions
                        selected_permutations.append(current_data)
                        break

    return selected_permutations


def make_question(dataset, seed):
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)][:-1].split(",")
    data = list(map(int, data))
    inserts = data[0:-4]
    deletions = data[-4:]
    final_keys = [x for x in inserts if x not in deletions]

    tree = BPlusTree(4)

    for x in inserts:
        tree.insert(x)
    for x in deletions:
        tree.delete(x)

    inserts_string = ", ".join(map(str, inserts))
    deletions_string = ", ".join(map(str, deletions))

    obscure = random.sample(final_keys, 3)

    question_string = f"""
    \\item{{
        Építsünk fel egy \(d = 4\) fokszámú \\textbf{{B+ fát}} a következő kulcsok beszúrásával: 
        \\textbf{{{inserts_string}}} ! Ezután töröljük sorrendben a 
        \\textbf{{{deletions_string}}} kulcsokat!\\\\[1em]
        A fa végső állapotában milyen kulcsok találhatóak az X,Y,Z helyeken?\\\\[1em]
        \\begin{{center}}
        {tree.print_in_latex(obscure)}
        \\end{{center}}
    }}
    """
    answer_string = f"""
    \\item{{
        Építsünk fel egy \(d = 4\) fokszámú \\textbf{{B+ fát}} a következő kulcsok beszúrásával: 
        \\textbf{{{inserts_string}}} ! Ezután töröljük sorrendben a 
        \\textbf{{{deletions_string}}} kulcsokat!\\\\[1em]
        A fa végső állapotában milyen kulcsok találhatóak az X,Y,Z helyeken?\\\\
        X: {obscure[0]}, Y: {obscure[1]}, Z: {obscure[2]}\\\\
        \\begin{{center}}
        {tree.print_in_latex()}
        \\end{{center}}
    }}
    """

    return question_string, answer_string


def print_dependencies():
    print(f"\\usetikzlibrary{{trees, arrows.meta,shapes.multipart}}")
    print(f"\\usepackage{{forest}}")
    print(f"\\newcommand\mpnc[3]{{\\nodepart{{one}} $#1$\\nodepart{{two}} $#2$\\nodepart{{three}} $#3$}}")
