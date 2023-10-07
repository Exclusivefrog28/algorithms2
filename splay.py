class SplayTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None

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
            if node == parent.left:
                self.right_rotate(parent)
            else:
                self.left_rotate(parent)

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

        if node.left is None and node.right == None:
            left_child, right_child = "", ""

        return f"node [circle,draw] {{{node.key}}} {left_child} {right_child}"
