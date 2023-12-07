import random


class HuffmanLeaf:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq


class HuffmanTree:
    def __init__(self, left=None, right=None):
        self.freq = left.freq + right.freq
        self.left = left
        self.right = right


def huffman(data):
    freq = {}
    for c in data:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    trees = []
    for key in freq:
        trees.append(HuffmanLeaf(key, freq[key]))

    while len(trees) > 1:
        trees.sort(key=lambda x: x.freq)
        left = trees.pop(0)
        right = trees.pop(0)
        trees.append(HuffmanTree(left, right))

    huffman_tree = trees[0]
    codes = {}

    def traverse(node, code):
        if isinstance(node, HuffmanLeaf):
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")

    traverse(huffman_tree, "")

    coded_string = ""

    for char in data:
        coded_string += codes[char]

    return freq, huffman_tree, codes, coded_string, len(coded_string) / (len(data) * 8)


def get_data_huffman(iterations):
    characters = ['A', 'S', 'I', 'O', 'X']
    frequencies = [8, 8, 4, 1, 1]
    dataset = []

    for iteration in range(iterations):
        random.shuffle(characters)
        elements = []
        for i in range(len(characters)):
            for j in range(frequencies[i]):
                elements.append(characters[i])
        random.shuffle(elements)
        data = ''.join(elements)
        if data not in dataset:
            dataset.append(data)
    return dataset


def print_tree(tree):
    def print_subtree(subtree):
        if isinstance(subtree, HuffmanLeaf):
            return f"node [minimum height=0.5cm,minimum width=0.5cm,draw] {{{subtree.char}}}"
        left_child = f"child {{{print_subtree(subtree.left)}}}"
        right_child = f"child {{{print_subtree(subtree.right)}}}"

        return f"node [circle,draw] {{{subtree.freq}}} {left_child} {right_child}"

    tree_string = "\\begin{tikzpicture}[level/.style={sibling distance=64mm/#1},transform shape]\n"
    tree_string += "\\" + print_subtree(tree) + ";"
    tree_string += "\\end{tikzpicture}\n"
    return tree_string


def make_question_huffman(dataset, seed):
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)][:-1]

    freq, tree, codes, coded_string, compression_ratio = huffman(data)

    leaves = list(codes.keys())

    question_string = f"""\\item{{
                Tömörítsük az alábbi 8-bites karaktersorozatot \\textbf{{Huffman-kóddal}}! Rajzoljuk fel a kódolás
                során készített \\textbf{{Huffman-fát}} a karaktersorozat alatt található levelek felé.
                A fa alapján írjuk fel a \\textbf{{kódtáblát}} és határozzuk meg a \\textbf{{tömörítési rátát}}!
                \\begin{{center}}
                {data}\\\\
                \\vspace{{3.5cm}}
                \\begin{{tikzpicture}}
                \\node [minimum height=0.5cm,minimum width=0.5cm,draw] at (0,0) {{{leaves[0]}}};
                \\node [minimum height=0.5cm,minimum width=0.5cm,draw] at (1.5,0) {{{leaves[1]}}};
                \\node [minimum height=0.5cm,minimum width=0.5cm,draw] at (3,0) {{{leaves[2]}}};
                \\node [minimum height=0.5cm,minimum width=0.5cm,draw] at (4.5,0) {{{leaves[3]}}};
                \\node [minimum height=0.5cm,minimum width=0.5cm,draw] at (6,0) {{{leaves[4]}}};
                \\end{{tikzpicture}}
                \\end{{center}}
        }}
        """

    answer_string = f"""\\item{{
                Tömörítsük az alábbi 8-bites karaktersorozatot \\textbf{{Huffman-kóddal}}! Rajzoljuk fel a kódolás
                során készített \\textbf{{Huffman-fát}} a karaktersorozat alatt található levelek felé.
                A fa alapján írjuk fel a \\textbf{{kódtáblát}} és határozzuk meg a \\textbf{{tömörítési rátát}}!
                \\begin{{center}}
                Frekvenciák: {freq}\\\\
                Kódok: {codes}\\\\
                Kódolt adat: {coded_string}\\\\
                Tömörítési ráta: {compression_ratio}\\\\
                \\vspace{{0.1cm}}
                {print_tree(tree)}
                \\end{{center}}
        }}
        """

    return question_string, answer_string
