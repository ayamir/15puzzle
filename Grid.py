# For direction
LEFT = 1
RIGHT = 2
UP = 4
DOWN = 8


class Grid(object):
    def __init__(self, nums: list):
        self.nums = nums
        self.parent = None
        self.G = 0
        self.H = 0
        self.L = 0

    def __hash__(self):
        return hash((tuple(self.nums), self.parent, self.G, self.H, self.L))

    def __eq__(self, other):
        return self.nums == other.nums

    # for PriorityQueue's sort
    def __lt__(self, other):
        return (self.G + self.H + self.L) < (other.G + other.H + other.L)

    # get blank's place
    def blank(self) -> int:
        return self.nums.index(0) + 1

    # judge solvable
    def is_solvable(self) -> bool:
        inv = cnt_inv(self.nums) - self.blank() + 1
        x = 4 - self.blank() // 4
        if (inv % 2) ^ (x % 2) == 1:
            return True
        else:
            return False

    def up(self):
        tmp_nums = self.nums.copy()
        old_blank = self.blank() - 1
        tmp_nums[old_blank] = tmp_nums[old_blank + 4]
        tmp_nums[old_blank + 4] = 0
        return Grid(tmp_nums)

    def down(self):
        tmp_nums = self.nums.copy()
        old_blank = self.blank() - 1
        tmp_nums[old_blank] = tmp_nums[old_blank - 4]
        tmp_nums[old_blank - 4] = 0
        return Grid(tmp_nums)

    def left(self):
        tmp_nums = self.nums.copy()
        old_blank = self.blank() - 1
        tmp_nums[old_blank] = tmp_nums[old_blank + 1]
        tmp_nums[old_blank + 1] = 0
        return Grid(tmp_nums)

    def right(self):
        tmp_nums = self.nums.copy()
        old_blank = self.blank() - 1
        tmp_nums[old_blank] = tmp_nums[old_blank - 1]
        tmp_nums[old_blank - 1] = 0
        return Grid(tmp_nums)

    def directions(self) -> int:
        res = 0
        if self.blank() == 1:
            res = LEFT + UP
        elif 1 < self.blank() < 4:
            res = LEFT + RIGHT + UP
        elif self.blank() == 4:
            res = RIGHT + UP
        elif self.blank() == 5 or self.blank() == 9:
            res = UP + DOWN + LEFT
        elif 5 < self.blank() < 8 or 9 < self.blank() < 12:
            res = UP + DOWN + LEFT + RIGHT
        elif self.blank() == 8 or self.blank() == 12:
            res = UP + DOWN + RIGHT
        elif self.blank() == 13:
            res = DOWN + LEFT
        elif 13 < self.blank() < 16:
            res = LEFT + RIGHT + DOWN
        elif self.blank() == 16:
            res = DOWN + RIGHT
        return res

    def children(self) -> list:
        res = []
        directions = self.directions()
        if directions == UP + LEFT:
            res.append(self.up())
            res.append(self.left())
        elif directions == UP + LEFT + RIGHT:
            res.append(self.up())
            res.append(self.left())
            res.append(self.right())
        elif directions == UP + RIGHT:
            res.append(self.up())
            res.append(self.right())
        elif directions == UP + DOWN + LEFT:
            res.append(self.up())
            res.append(self.down())
            res.append(self.left())
        elif directions == UP + DOWN + RIGHT:
            res.append(self.up())
            res.append(self.down())
            res.append(self.right())
        elif directions == UP + DOWN + LEFT + RIGHT:
            res.append(self.up())
            res.append(self.down())
            res.append(self.left())
            res.append(self.right())
        elif directions == DOWN + LEFT:
            res.append(self.down())
            res.append(self.left())
        elif directions == DOWN + LEFT + RIGHT:
            res.append(self.down())
            res.append(self.left())
            res.append(self.right())
        elif directions == DOWN + RIGHT:
            res.append(self.down())
            res.append(self.right())
        return res


def cnt_inv(nums: list) -> int:
    inv = 0
    for i in range(len(nums)):
        for k in range(i + 1, len(nums)):
            if nums[i] > nums[k]:
                inv += 1
    return inv
