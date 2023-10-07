class AVLTreeNode:
    def __init__(self, key):
        self.key = key
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

    def insert(self, key):
        if self.root is None:
            self.root = AVLTreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = AVLTreeNode(key)
                node.left.parent = node
                self.rebalance(node)
            else:
                self._insert(node.left, key)

        else:
            if node.right is None:
                node.right = AVLTreeNode(key)
                node.right.parent = node
                self.rebalance(node)
            else:
                self._insert(node.right, key)

    def rebalance(self, node):
        self.calculate_heights(node)

        if node.balance == 2:
            if node.right.balance == -1:
                self.right_rotate(node.right)
                self.double_rotations += 1
            else:
                self.single_rotations += 1
            self.left_rotate(node)
        elif node.balance == -2:
            if node.left.balance == 1:
                self.left_rotate(node.left)
                self.double_rotations += 1
            else:
                self.single_rotations += 1
            self.right_rotate(node)
        elif node.parent is not None:
            self.rebalance(node.parent)

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

        self.calculate_heights(new_root.right)
        self.calculate_heights(new_root)

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

        self.calculate_heights(new_root.left)
        self.calculate_heights(new_root)

    def calculate_heights(self, node):
        left_height = node.left.height if node.left is not None else 0
        right_height = node.right.height if node.right is not None else 0
        node.height = 1 + max(left_height, right_height)
        node.balance = right_height - left_height

    def print_tree_in_latex(self):
        tree_string = self._print_tree_in_latex_helper(self.root)

        print(f"\\begin{{tikzpicture}}[level/.style={{sibling distance=60mm/#1}}]")
        print(f"\\{tree_string};")
        print(f"\\end{{tikzpicture}}")
        print(f"\\\[20pt]")

    def _print_tree_in_latex_helper(self, node):
        if node is None:
            return ""

        left_child = f"child {{{self._print_tree_in_latex_helper(node.left)}}}" if node.left is not None else "child[missing]"
        right_child = f"child {{{self._print_tree_in_latex_helper(node.right)}}}" if node.right is not None else "child[missing]"

        if node.left is None and node.right is None:
            left_child, right_child = "", ""

        return f"node [circle,draw] {{{node.key}}} {left_child} {right_child}"
