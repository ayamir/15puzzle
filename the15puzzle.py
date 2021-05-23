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
    def count_inversions(num_order):
        inversions = 0
        for i in range(len(num_order) - 1):
            for k in range(i + 1, len(num_order)):
                if num_order[i] > num_order[k]:
                    inversions += 1
        return inversions

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

    while count_inversions(num_list) % 2 != 0:
        random.shuffle(num_list)

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


class Grid:
    def __init__(self, g: int, num_list: list[int]):
        self.nums = num_list
        self.g = g
        self.h = manhattan(self.nums)

    def blank(self) -> int:
        return self.nums.index(0) + 1

    def direction(self) -> int:
        directions = 0
        if self.blank() == 1:
            directions = LEFT + UP
        elif 1 < self.blank() < 4:
            directions = LEFT + RIGHT + UP
        elif self.blank() == 4:
            directions = RIGHT + UP
        elif self.blank() == 5 or self.blank() == 9:
            directions = UP + DOWN + LEFT
        elif 5 < self.blank() < 8 or 9 < self.blank() < 12:
            directions = UP + DOWN + LEFT + RIGHT
        elif self.blank() == 8 or self.blank() == 12:
            directions = UP + DOWN + RIGHT
        elif self.blank() == 13:
            directions = DOWN + LEFT
        elif self.blank() == 16:
            directions = DOWN + RIGHT
        elif 13 < self.blank() < 16:
            directions = LEFT + RIGHT + DOWN
        return directions

    def up(self):
        new_nums = self.nums.copy()
        old_blank = self.blank() - 1
        new_nums[old_blank] = new_nums[old_blank + 4]
        new_nums[old_blank + 4] = 0
        return Grid(0, new_nums)

    def down(self):
        new_nums = self.nums.copy()
        old_blank = self.blank() - 1
        new_nums[old_blank] = new_nums[old_blank - 4]
        new_nums[old_blank - 4] = 0
        return Grid(0, new_nums)

    def left(self):
        new_nums = self.nums.copy()
        old_blank = self.blank() - 1
        new_nums[old_blank] = new_nums[old_blank - 1]
        new_nums[old_blank - 1] = 0
        return Grid(0, new_nums)

    def right(self):
        new_nums = self.nums.copy()
        old_blank = self.blank() - 1
        new_nums[old_blank] = new_nums[old_blank + 1]
        new_nums[old_blank + 1] = 0
        return Grid(0, new_nums)

    def children(self) -> list:
        children = []
        directions = self.direction()
        if directions == UP + LEFT:
            children.append((self.up(), UP))
            children.append((self.left(), LEFT))
        elif directions == UP + LEFT + RIGHT:
            children.append((self.left(), LEFT))
            children.append((self.right(), RIGHT))
            children.append((self.up(), UP))
        elif directions == UP + RIGHT:
            children.append((self.up(), UP))
            children.append((self.right(), RIGHT))
        elif directions == UP + DOWN + LEFT:
            children.append((self.up(), UP))
            children.append((self.down(), DOWN))
            children.append((self.left(), LEFT))
        elif directions == UP + DOWN + RIGHT:
            children.append((self.up(), UP))
            children.append((self.down(), DOWN))
            children.append((self.right(), RIGHT))
        elif directions == UP + DOWN + LEFT + RIGHT:
            children.append((self.up(), UP))
            children.append((self.down(), DOWN))
            children.append((self.left(), LEFT))
            children.append((self.right(), RIGHT))
        elif directions == DOWN + LEFT:
            children.append((self.down(), DOWN))
            children.append((self.left(), LEFT))
        elif directions == DOWN + LEFT + RIGHT:
            children.append((self.down(), DOWN))
            children.append((self.left(), LEFT))
            children.append((self.right(), RIGHT))
        elif directions == DOWN + RIGHT:
            children.append((self.down(), DOWN))
            children.append((self.right(), RIGHT))
        return children


def manhattan(num_list: list[int]) -> int:
    h = 0
    for value in range(1, 16):
        _x = value // 4
        _y = value % 4
        index = num_list.index(value) + 1
        x = index // 4
        y = index % 4
        h += abs(_x - x) + abs(_y - y)
    return h


if __name__ == "__main__":
    methods = []
    # Use 0 as blank
    init = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    goal = nums.copy()
    random.shuffle(nums)
    initial_grid = Grid(0, init)
    # open_dict and close_dict contain like this: (Grid, UP)
    open_dict = {}
    close_dict = {}
    open_dict[initial_grid] = 0

    while open_dict:
        current = min(open_dict.keys(), key=lambda k: k.g + k.h)
        method = open_dict.get(current)
        if method != 0:
            methods.append(method)
        if current.nums == goal:
            break
        open_dict.pop(current)
        close_dict[current] = method
        for node_tuple in current.children():
            node = node_tuple[0]
            direction = node_tuple[1]
            if node in close_dict:
                continue
            if node in open_dict:
                new_g = current.g + 1
                if new_g < node.g:
                    node.g = new_g
                    open_dict[node] = direction
            else:
                node.g = current.g + 1
                open_dict[node] = direction

    gui(methods, init)
