import random


def init_shift(alphabet, pattern):
    shift = {}
    for i in range(len(alphabet)):
        shift[alphabet[i]] = len(pattern) + 1
    for j in range(len(pattern)):
        shift[pattern[j]] = len(pattern) - j
    return shift


def quicksearch(text, pattern):
    alphabet = list(set(text))
    alphabet.sort()
    shift = init_shift(alphabet, pattern)
    comparisons = 0
    matches = []
    len_text = len(text)
    len_pattern = len(pattern)
    i = 0
    while i + len_pattern <= len_text:
        match = True
        for j in range(i, i + len_pattern):
            comparisons += 1
            if text[j] != pattern[j - i]:
                match = False
                break
        if match:
            matches.append(i + 1)

        if i + len_pattern < len_text:
            i += shift[text[i + len_pattern]]
        else:
            break

    return comparisons, matches, shift


def get_data_quicksearch(iterations, comparisons, matches):
    characters = ['A', 'S', 'T', 'O', 'X']
    len_data = 20
    len_pattern = 7
    dataset = []

    for iteration in range(iterations):
        data = ''.join(random.choices(characters, k=len_data))
        pattern = ''.join(random.choices(characters, k=len_pattern))
        current_comparisons, current_matches, shift = quicksearch(data, pattern)
        if current_comparisons in comparisons and len(current_matches) == matches:
            if data not in dataset:
                dataset.append(f'{data}-{pattern}')
    return dataset


def make_question_quicksearch(dataset, seed):
    random.seed(seed)
    data = dataset[random.randint(0, len(dataset) - 1)][:-1]
    data = data.split('-')
    text, pattern = data[0], data[1]

    comparisons, matches, shift = quicksearch(text, pattern)

    question_string = f"""\\item{{
                Adott az alábbi \\textbf{{S}} szöveg és \\textbf{{M}} minta. Szemléltesse a \\textbf{{gyorskeresés (quicksearch)}} 
                algoritmus működését! Adja meg a \\textbf{{SHIFT vektor értékeit}}! Rajzolja le a szöveg alá a 
                \\textbf{{minta eltolásait}} és adja meg, hogy pontosan hány \\textbf{{összehasonlítást}} végez az 
                algoritmus! Összehasonlításnak tekintse a minta és szöveg egy—egy karakterének az összehasonlítását!
                \\begin{{center}}
                S = {text}\\\\
                M = {pattern}\\\\
                \\vspace{{0.5cm}}
                \\begin{{tabular}}{{|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}
                |x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}
                |x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|x{{0.4cm}}|}}
                \\hline
                {' & '.join(text)}\\\\
                \\hline
                {' & '.join(pattern)} & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                & & & & & & & & & & & & & & & & & & &\\\\
                \\hline
                \\end{{tabular}}
                \\end{{center}}
        }}
        """

    answer_string = f"""\\item{{
                Adott az alábbi \\textbf{{S}} szöveg és \\textbf{{M}} minta. Szemléltesse a \\textbf{{gyorskeresés (quicksearch)}} 
                algoritmus működését! Adja meg a \\textbf{{SHIFT vektor értékeit}}! Rajzolja le a szöveg alá a 
                \\textbf{{minta eltolásait}} és adja meg, hogy pontosan hány \\textbf{{összehasonlítást}} végez az 
                algoritmus! Összehasonlításnak tekintse a minta és szöveg egy—egy karakterének az összehasonlítását!
                \\begin{{center}}
                Összehasonlítások száma: {comparisons}\\\\
                Helyes eltolások: {matches}\\\\
                SHIFT:  {shift}                
                \\end{{center}}
        }}
        """

    return question_string, answer_string
