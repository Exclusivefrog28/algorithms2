import copy
import random

from bellmanford import make_question_bellmanford, get_edgesets_bellmanford
from bfs import make_question_bfs, get_edgesets_bfs
from dijkstra import make_question_dijkstra, get_edgesets_dijkstra
from floyd import make_question_floyd
from huffman import make_question_huffman, get_data_huffman
from prim import make_question_prim, get_edgesets_prim
from quicksearch import make_question_quicksearch, get_data_quicksearch


def make_quiz(count, seed):
    random.seed(seed)

    with open("exam-two/bfs.txt", "r") as f:
        bfs_dataset = f.readlines()
        f.close()
    with open("exam-two/dijkstra.txt", "r") as f:
        dijkstra_dataset = f.readlines()
        f.close()
    with open("exam-two/bellmanford.txt", "r") as f:
        bellmanford_dataset = f.readlines()
        f.close()
    with open("exam-two/prim.txt", "r") as f:
        prim_dataset = f.readlines()
        f.close()
    with open("exam-two/huffman.txt", "r") as f:
        huffman_dataset = f.readlines()
        f.close()
    with open("exam-two/quicksearch.txt", "r") as f:
        quicksearch_dataset = f.readlines()
        f.close()

    exam_string = """\\documentclass{article}
        \\usepackage[a4paper, margin=0.7in]{geometry}
        \\usepackage{tikz}
        \\usepackage{array}
        \\usepackage{amsmath}
        \\usepackage{arydshln}
        \\usepackage{multirow}
        \\usepackage{multicol}
        \\usetikzlibrary{trees, arrows.meta,}
        \\usetikzlibrary{graphs,graphdrawing,trees,arrows.meta,shapes.multipart}
        \\usetikzlibrary{quotes}
        \\tikzset{graphs/simpleer/.style={nodes={draw, circle},node distance=1.75cm, nodes={minimum size=2em}}}
        \\usegdlibrary{circular,force,layered,routing}
        \\newcolumntype{x}[1]{>{\\centering\\arraybackslash}p{#1}}
        \\renewcommand{\\arraystretch}{1.5}
        \\begin{document}
        """
    answer_string = copy.copy(exam_string)

    for i in range(count):
        seed = ''.join(random.choice('123456789ABCDEFGHJKLMNOPQRSTUVWXYZ') for i in range(6))
        bfs_q, bfs_a = make_question_bfs(bfs_dataset, seed)
        dijkstra_q, dijkstra_a = make_question_dijkstra(dijkstra_dataset, seed)
        bellmanford_q, bellmanford_a = make_question_bellmanford(bellmanford_dataset, seed)
        floyd_q, floyd_a = make_question_floyd(bellmanford_dataset, seed)
        prim_q, prim_a = make_question_prim(prim_dataset, seed)
        huffman_q, huffman_a = make_question_huffman(huffman_dataset, seed)
        quicksearch_q, quicksearch_a = make_question_quicksearch(quicksearch_dataset, seed)
        exam_first_page = f"""\\vspace*{{-0.6in}}
                \\noindent
                {{\\hspace*{{-0.3 in}}Név:\\hfill {seed}\\\\
                \\hspace*{{-0.3 in}}Neptun kód:}}
                \\begin{{center}}
                    \\large{{
                    \\textbf{{
                        Algoritmusok és adatszerkezetek II. gyakorlat\\\\
                        Zárthelyi dolgozat – 2. témakör
                        }}\\\\
                    2023. december 12.
                    }}
                \\end{{center}}
                \\begin{{enumerate}}
                    {bfs_q}
                    {dijkstra_q}
                    {bellmanford_q}
                    {floyd_q}
                \\end{{enumerate}}
                \\thispagestyle{{empty}}
                \\newpage"""
        exam_second_page = f"""\\vspace*{{-0.6in}}
                \\noindent
                {{\\hspace*{{-0.6 in}}Név:\\hfill {seed}\\\\
                \\hspace*{{-0.6 in}}Neptun kód:}}
                \\thispagestyle{{empty}}
                    \\vspace*{{1em}}
                    \\begin{{enumerate}}
                    \\setcounter{{enumi}}{{4}}
                    {prim_q}
                    {huffman_q}
                    {quicksearch_q}
                \\end{{enumerate}}
                \\newpage
        """
        answer_first_page = f"""\\vspace*{{-0.6in}}
                \\noindent
                {{\\hspace*{{-0.3 in}}Név:\\hfill {seed}\\\\
                \\hspace*{{-0.3 in}}Neptun kód:}}
                \\begin{{center}}
                    \\large{{
                    \\textbf{{
                        Algoritmusok és adatszerkezetek II. gyakorlat\\\\
                        Zárthelyi dolgozat – 2. témakör - MEGOLDÁSOK
                        }}\\\\
                    2023. december 12.
                    }}
                \\end{{center}}
                \\begin{{enumerate}}
                    {bfs_a}
                    {dijkstra_a}
                    {bellmanford_a}
                    {floyd_a}
                \\end{{enumerate}}
                \\thispagestyle{{empty}}
                \\newpage"""
        answer_second_page = f"""\\vspace*{{-0.6in}}
                \\noindent
                {{\\hspace*{{-0.6 in}}Név:\\hfill {seed}\\\\
                \\hspace*{{-0.6 in}}Neptun kód:}}
                \\thispagestyle{{empty}}
                    \\vspace*{{1em}}
                    \\begin{{enumerate}}
                    \\setcounter{{enumi}}{{4}}
                    {prim_a}
                    {huffman_a}
                    {quicksearch_a}
                \\end{{enumerate}}
                \\newpage
        """
        exam_string += exam_first_page + exam_second_page
        answer_string += answer_first_page + answer_second_page

    exam_string += "\n\\end{document}"
    answer_string += "\n\\end{document}"

    with open(f"exam-two/Algo2ZH2-20231212.tex", "w", encoding="utf-8") as f:
        f.write(exam_string)
        f.close()
    with open(f"exam-two/Algo2ZH2megoldasok-20231212.tex", "w", encoding="utf-8") as f:
        f.write(answer_string)
        f.close()


def create_bfs_dataset():
    selected_edgesets = get_edgesets_bfs(100000, [7], 1)

    with open("exam-two/bfs.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_dijkstra_dataset():
    selected_edgesets = get_edgesets_dijkstra(100000, [2, 3])

    with open("exam-two/dijkstra.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_bellmanford_dataset():
    selected_edgesets = get_edgesets_bellmanford(100000, [8, 9, 10])

    with open("exam-two/bellmanford.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_prim_dataset():
    selected_edgesets = get_edgesets_prim(5000)

    with open("exam-two/prim.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_huffman_dataset():
    dataset = get_data_huffman(10000)

    with open("exam-two/huffman.txt", "w") as f:
        for d in dataset:
            f.write(d + "\n")
        f.close()


def create_quicksearch_dataset():
    dataset = get_data_quicksearch(50000000, [10, 11, 12], 1)

    with open("exam-two/quicksearch.txt", "w") as f:
        for d in dataset:
            f.write(d + "\n")
        f.close()
