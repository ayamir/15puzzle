import random
import time

import pygame

# For direction
LEFT = 1
RIGHT = 2
UP = 4
DOWN = 8

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((598, 598))
screen.fill((0, 0, 0))
pygame.display.set_caption("Arrange the Numbers!")
font = pygame.font.Font('fonts/Adca.ttf', 35)
clock = pygame.time.Clock()
victory = pygame.mixer.Sound("sounds/TaDa.ogg")


class Tile(object):
    def __init__(self, num, x, y):
        self.number = num
        self.x = x
        self.y = y
        self.width = 99
        self.height = 99

    def draw(self):
        pygame.draw.rect(screen, RED,
                         (self.x, self.y, self.width, self.height), 0)
        text = font.render(str(self.number), True, WHITE)
        textRect = text.get_rect(center=((2 * self.x + self.width) / 2,
                                         (2 * self.y + self.height) / 2))
        screen.blit(text, textRect)

    def moveIt(self, dist):
        final_x = self.x + dist[0]
        final_y = self.y + dist[1]

        while self.x != final_x or self.y != final_y:
            screen.fill(WHITE, [self.x, self.y, 99, 99])
            self.x += int(dist[0] / 50)
            self.y += int(dist[1] / 50)
            self.draw()
            pygame.display.update()

        clock.tick(60)


def gui(action_sequence: list, num_list: list):
    def moves_display(my_text):
        txt = font.render(my_text, True, WHITE)
        textRect = txt.get_rect(center=(299, 550))
        screen.blit(txt, textRect)

    def show_congrats():
        txt = font.render("Congratulations! You did it!", True, GREEN)
        textRect = txt.get_rect(center=(299, 49))
        screen.blit(txt, textRect)
        pygame.display.update()
        print("\nYou solved it! Game window closing in 10 seconds....")

    listOfTiles = []
    move_counter = 0
    index = 0
    empty_x = 0
    empty_y = 0

    pygame.draw.rect(screen, WHITE, (98, 98, 403, 403))
    for y in range(100, 500, 100):
        for x in range(100, 500, 100):
            if index < 16:
                da_num = num_list[index]
                if da_num != 0:
                    new_tile = Tile(da_num, x, y)
                    listOfTiles.append(new_tile)
                    new_tile.draw()
                else:
                    empty_x = x
                    empty_y = y
                index += 1

    pygame.display.update()

    for action in action_sequence:
        xy_dist = [None, None]

        if action == LEFT:
            xy_dist = [-100, 0]
        elif action == RIGHT:
            xy_dist = [100, 0]
        elif action == UP:
            xy_dist = [0, -100]
        elif action == DOWN:
            xy_dist = [0, 100]

        for tile in listOfTiles:
            if tile.x + xy_dist[0] == empty_x and tile.y + xy_dist[1] == empty_y:
                move_counter += 1
                empty_x = tile.x
                empty_y = tile.y
                tile.moveIt(xy_dist)
                break

    screen.fill(BLACK, [200, 515, 200, 85])
    moves_display("Moves: " + str(move_counter))
    pygame.display.update()
    clock.tick(60)

    show_congrats()
    victory.play()
    time.sleep(3)


class Grid(object):
    def __init__(self, nums: list):
        self.nums = nums
        self.parent = None
        self.G = 0
        self.H = 0

    def __hash__(self):
        return hash((tuple(self.nums), self.parent, self.G, self.H))

    def __eq__(self, other):
        return self.nums == other.nums

    def blank(self) -> int:
        return self.nums.index(0) + 1

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
        if self.blank() == 1:
            return LEFT + UP
        elif 1 < self.blank() < 4:
            return LEFT + RIGHT + UP
        elif self.blank() == 4:
            return RIGHT + UP
        elif self.blank() == 5 or self.blank() == 9:
            return UP + DOWN + LEFT
        elif 5 < self.blank() < 8 or 9 < self.blank() < 12:
            return UP + DOWN + LEFT + RIGHT
        elif self.blank() == 8 or self.blank() == 12:
            return UP + DOWN + RIGHT
        elif self.blank() == 13:
            return DOWN + LEFT
        elif 13 < self.blank() < 16:
            return LEFT + RIGHT + DOWN
        elif self.blank() == 16:
            return DOWN + RIGHT

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


def get_inv_count(a: list) -> int:
    inv_count = 0
    removed = a.copy()
    removed.remove(0)
    n = len(removed)
    for i in range(n):
        for j in range(i + 1, n):
            if removed[i] > removed[j]:
                inv_count += 1
    return inv_count


def count_inversions(num_order):
    inversions = 0
    for i in range(len(num_order) - 1):
        for k in range(i + 1, len(num_order)):
            if num_order[i] > num_order[k]:
                inversions += 1
    return inversions


def a_star(grid: Grid) -> list:
    open_set = set()
    close_set = set()
    open_set.add(grid)
    while open_set:
        current = min(open_set, key=lambda k: k.G + k.H)
        current_nums = current.nums
        if current_nums == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
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
                node.parent = current
                open_set.add(node)


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
    init = [2, 5, 3, 4, 1, 0, 6, 8, 9, 13, 7, 11, 14, 10, 15, 12]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    while not count_inversions(init) % 2 != 0:
        random.shuffle(init)
    else:
        print(init)
        paths = a_star(Grid(init))
        gui(get_methods(paths), init)
