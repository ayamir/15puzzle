import time

from Grid import *


def a_star(grid: Grid, goal):
    start_time = time.process_time()
    open_set = set()
    close_set = set()
    open_set.add(grid)
    while open_set:
        current = min(open_set, key=lambda k: k.G + k.H + 2 * k.L)
        current_nums = current.nums
        for i in range(4):
            for j in range(4):
                print(current_nums[i * 4 + j], end=' ')
            print()
        print()
        current_time = time.process_time()
        elapsed_time = current_time - start_time
        if current_nums == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1], elapsed_time
        if elapsed_time > 300:
            return [], elapsed_time
        open_set.remove(current)
        close_set.add(current)
        for node in current.children():
            if node in close_set:
                continue
            if node in open_set:
                new_g = current.G + 1
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
            else:
                node.G = current.G + 1
                node.H = manhattan(node.nums)
                node.L = linear_conflicts(node.nums, goal)
                node.parent = current
                open_set.add(node)


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
