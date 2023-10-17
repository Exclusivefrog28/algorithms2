import avl
import bplus
import splay


# with open("splay.txt", "r") as f:
#     dataset = f.readlines()
#     f.close()
# question, answer = splay.make_question(dataset, "seed")
# print(question)
# print(answer)

# with open("bplus.txt", "r") as f:
#     dataset = f.readlines()
#     f.close()
# question, answer = bplus.make_question(dataset, "seed")
# print(question)
# print(answer)

# with open("avl_1s_1d.txt", "r") as f:
#     dataset = f.readlines()
#     f.close()
# question, answer = avl.make_question(dataset, "seed")
# print(question)
# print(answer)

# with open("avl_3s_0d.txt", "r") as f:
#     dataset = f.readlines()
#     f.close()
# question, answer = avl.make_question(dataset, "seed")
# print(question)
# print(answer)


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
