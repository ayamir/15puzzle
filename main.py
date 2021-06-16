import random

from Astar import *
from GUI import *


def get_action(a: list, b: list) -> int:
    offset = b.index(0) - a.index(0)
    if offset == 1:
        return LEFT
    elif offset == -1:
        return RIGHT
    elif offset == 4:
        return UP
    elif offset == -4:
        return DOWN
    else:
        return 0


def get_methods(sequence: list) -> list:
    methods = []
    for i, v in enumerate(sequence):
        if i == len(sequence) - 1:
            break
        methods.append(get_action(v.nums, sequence[i + 1].nums))
    return methods


if __name__ == "__main__":
    # Use 0 as blank
    # init = [1, 0, 6, 4, 9, 5, 2, 8, 10, 14, 3, 7, 13, 15, 12, 11]
    init = [13, 2, 10, 3, 1, 12, 8, 4, 5, 0, 9, 6, 15, 14, 11, 7]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    start = Grid(init)
    while not start.isSolvable():
        random.shuffle(init)
        start = Grid(init)
    else:
        paths, elapsed_time = a_star(start, goal)
        if paths:
            gui(get_methods(paths), init, elapsed_time)
        else:
            print("elapsed over 5 minutes, program will end.")
