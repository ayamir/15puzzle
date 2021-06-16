from queue import PriorityQueue

from Grid import *

map = {}


def a_star(grid: Grid, goal: list):
    open_set = PriorityQueue()
    close_set = set()
    open_set.put(grid)
    while open_set.not_empty:
        current = open_set.get()
        current_nums = current.nums

        # omit existed state
        if map.__contains__(str(current_nums)):
            continue
        map[str(current_nums)] = 1

        # get answer
        if current_nums == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

        # add current grid to close set
        close_set.add(current)

        # iterate all current's children
        for node in current.children():
            if node in close_set:
                continue
            node.G = current.G + 1
            node.H = manhattan(node.nums)
            node.L = 2 * linear_conflicts(node.nums, goal)
            node.parent = current
            open_set.put(node)


def manhattan(nums: list) -> int:
    H = 0
    for value in range(1, 16):
        _x = value // 4
        _y = value % 4
        index = nums.index(value) + 1
        x = index // 4
        y = index % 4
        H += abs(_x - x) + abs(_y - y)
    return H


def linear_conflicts(candidate, solved):
    def count_conflicts(candidate_row, solved_row, ans=0):
        counts = [0 for _ in range(4)]
        for i, tile_1 in enumerate(candidate_row):
            if tile_1 in solved_row and tile_1 != 0:
                for j, tile_2 in enumerate(candidate_row):
                    if tile_2 in solved_row and tile_2 != 0:
                        if tile_1 != tile_2:
                            if (solved_row.index(tile_1) >
                                solved_row.index(tile_2)) and \
                                    i < j:
                                counts[i] += 1
                            if (solved_row.index(tile_1) <
                                solved_row.index(tile_2)) and \
                                    i > j:
                                counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            candidate_row[i] = -1
            ans += 1
            return count_conflicts(candidate_row, solved_row, ans)

    res = manhattan(candidate)
    candidate_rows = [[] for _ in range(4)]
    candidate_columns = [[] for _ in range(4)]
    solved_rows = [[] for _ in range(4)]
    solved_columns = [[] for _ in range(4)]
    for y in range(4):
        for x in range(4):
            idx = (y * 4) + x
            candidate_rows[y].append(candidate[idx])
            candidate_columns[x].append(candidate[idx])
            solved_rows[y].append(solved[idx])
            solved_columns[x].append(solved[idx])
    for k in range(4):
        res += count_conflicts(candidate_rows[k], solved_rows[k], 4)
    for k in range(4):
        res += count_conflicts(candidate_columns[k], solved_columns[k], 4)
    return res
