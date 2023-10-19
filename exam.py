import copy
import random

import avl
import bplus
import splay
import graph


def make_quiz(count, seed, print_twosided=False, reverse=False):
    random.seed(seed)

    with open("avl_3s_0d.txt", "r") as f:
        avl_dataset_1 = f.readlines()
        f.close()
    with open("avl_1s_1d.txt", "r") as f:
        avl_dataset_2 = f.readlines()
        f.close()
    with open("bplus.txt", "r") as f:
        bplus_dataset = f.readlines()
        f.close()
    with open("splay.txt", "r") as f:
        splay_dataset = f.readlines()
        f.close()
    with open("dfs.txt", "r") as f:
        dfs_dataset = f.readlines()
        f.close()
    with open("reduction.txt", "r") as f:
        reduction_dataset = f.readlines()
        f.close()

    exam_string = """\\documentclass{article}
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
    """

    answer_string = copy.copy(exam_string)

    exam_first_pages = []
    exam_second_pages = []
    answer_first_pages = []
    answer_second_pages = []

    answers = []

    for i in range(count):
        seed = ''.join(random.choice('123456789ABCDEFGHJKLMNOPQRSTUVWXYZ') for i in range(6))

        avl_question_1, avl_answer_1, avl_solution_1 = avl.make_question(avl_dataset_1, seed)
        avl_question_2, avl_answer_2, avl_solution_2 = avl.make_question(avl_dataset_2, seed)
        bplus_question, bplus_answer, bplus_solution = bplus.make_question(bplus_dataset, seed)
        splay_question, splay_answer, splay_solution = splay.make_question(splay_dataset, seed)
        dfs_question, dfs_answer, dfs_solution = graph.make_question_dfs(dfs_dataset, seed)
        reduction_question, reduction_answer, reduction_solution = graph.make_question_reduction(reduction_dataset,
                                                                                                 seed)

        answer = [seed] + avl_solution_1 + avl_solution_2 + bplus_solution + splay_solution + dfs_solution + reduction_solution
        answers.append(answer)

        exam_first_page = f"""\\vspace*{{-0.6in}}
        \\noindent
        {{\\hspace*{{-0.3 in}}Név:\\hfill {seed}\\\\
        \\hspace*{{-0.3 in}}Neptun kód:}}
        \\begin{{center}}
            \\large{{
            \\textbf{{
                Algoritmusok és adatszerkezetek II. gyakorlat\\\\
                Zárthelyi dolgozat – 1. témakör
                }}\\\\
            2023. október 24.
            }}
        \\end{{center}}
        \\begin{{enumerate}}
            \\item {{
                \\textbf{{Készítsen AVL-fát}} az alábbi kulcsok (adatok) megadott sorrend szerinti beszúrásával!
                Ha elromlott a fa kiegyensúlyozása, állítsa helyre a megfelelő forgatással!
                A fa elkészítése után \\textbf{{válaszoljon az alábbi kérdésekre}}! (\\textit{{Egy kettős forgatás egy balra és egy jobbra forgatásnak számít.}})
                \\begin{{enumerate}}
                {avl_question_1}
                {avl_question_2}
                \\end{{enumerate}}
            }}
            {bplus_question}
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
            \\setcounter{{enumi}}{{2}}
            {splay_question}
            \\vspace{{1em}}
            {dfs_question}
            \\vspace{{1em}}
            {reduction_question}
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
                Zárthelyi dolgozat – 1. témakör - MEGOLDÁSOK
                }}\\\\
            2023. október 24.
            }}
        \\end{{center}}
        \\begin{{enumerate}}
            \\item {{
                \\textbf{{Készítsen AVL-fát}} az alábbi kulcsok (adatok) megadott sorrend szerinti beszúrásával!
                Ha elromlott a fa kiegyensúlyozása, állítsa helyre a megfelelő forgatással!
                A fa elkészítése után \\textbf{{válaszoljon az alábbi kérdésekre}}! (\\textit{{Egy kettős forgatás egy balra és egy jobbra forgatásnak számít.}})
                \\begin{{enumerate}}
                {avl_answer_1}
                {avl_answer_2}
                \\end{{enumerate}}
            }}
            {bplus_answer}
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
            \\setcounter{{enumi}}{{2}}
            {splay_answer}
            \\vspace{{1em}}
            {dfs_answer}
            \\vspace{{1em}}
            {reduction_answer}
        \\end{{enumerate}}
        \\newpage
        """

        exam_string += exam_first_page
        answer_string += answer_first_page

        if print_twosided:
            exam_string += exam_second_page
            answer_string += answer_second_page
        else:
            exam_second_pages.append(exam_second_page)
            answer_second_pages.append(answer_second_page)

    if reverse:
        exam_second_pages.reverse()
        answer_second_pages.reverse()

    if not print_twosided:
        for page in exam_second_pages:
            exam_string += page
        for page in answer_second_pages:
            answer_string += page

    exam_string += "\n\\end{document}"
    answer_string += "\n\\end{document}"

    with open(f"exam{'_p' if not print_twosided else ''}{'_r' if reverse else ''}.tex", "w", encoding="utf-8") as f:
        f.write(exam_string)
        f.close()
    with open(f"answers{'_p' if not print_twosided else ''}{'_r' if reverse else ''}.tex", "w", encoding="utf-8") as f:
        f.write(answer_string)
        f.close()

    answers.sort(key=lambda x: x[0])

    with open(f"short_answers_trees.tex", "w", encoding="utf-8") as f:
        for a in answers:
            f.write(" & ".join(map(str, a[:9] + [a[0]])) + "\\\\\n")
            f.write("\\hline\n")
        f.close()

    with open(f"short_answers_graphs.tex", "w", encoding="utf-8") as f:
        for a in answers:
            f.write(" & ".join(map(str, [a[0]] + a[9:] + [a[0]])) + "\\\\\n")
            f.write("\\hline\n")
        f.close()


def create_avl_dataset():
    data = [40, 90, 20, 100, 60, 10, 110, 30, 50, 80, 70]
    selected_permutations = avl.get_permutations(data, 100000, 1, 1)

    with open("avl_1s_1d.txt", "w") as f:
        for p in selected_permutations:
            f.write(str(",".join(map(str, p))) + "\n")
        f.close()


def create_bplus_dataset():
    data = [2, 15, 20, 3, 9, 19, 12, 14, 10, 11, 13, 17]
    selected_permutations = bplus.get_permutations(data, 10000, 5, 1, 0, 2, 1)

    with open("bplus.txt", "w") as f:
        for p in selected_permutations:
            f.write(str(",".join(map(str, p))) + "\n")
        f.close()


def create_splay_dataset():
    data = [70, 90, 40, 30, 100, 50, 20, 60]
    selected_permutations = splay.get_permutations(data, 100000, 3, 8)

    with open("splay.txt", "w") as f:
        for p in selected_permutations:
            f.write(str(",".join(map(str, p))) + "\n")
        f.close()


def create_dfs_dataset():
    data = [[0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]]

    selected_edgesets = graph.get_edgesets_dfs(data, 1000000, 11, 3)

    with open("dfs.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()


def create_reduction_dataset():
    selected_edgesets = graph.get_edgesets_reduction(7, 100000, 3)

    with open("reduction.txt", "w") as f:
        for es in selected_edgesets:
            string = ""
            for row in es:
                string += str(" ".join(map(str, row))) + " "
            string = string[:-1]
            f.write(string + "\n")
        f.close()
