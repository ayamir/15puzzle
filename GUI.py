import time

import pygame

from Grid import DOWN
from Grid import LEFT
from Grid import RIGHT
from Grid import UP

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((598, 598))
screen.fill((0, 0, 0))
pygame.display.set_caption("Arrange the Numbers!")
font = pygame.font.Font('fonts/RobotoMono-Bold.ttf', 35)
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

    def move_it(self, dest):
        final_x = self.x + dest[0]
        final_y = self.y + dest[1]

        while self.x != final_x or self.y != final_y:
            screen.fill(WHITE, [self.x, self.y, 99, 99])
            self.x += int(dest[0] / 50)
            self.y += int(dest[1] / 50)
            self.draw()
            pygame.display.update()

        clock.tick(60)


def gui(action_sequence: list, num_list: list, elapsed_time: float):
    def moves_display(my_text):
        txt = font.render(my_text, True, WHITE)
        textRect = txt.get_rect(center=(299, 550))
        screen.blit(txt, textRect)

    def show_congrats():
        txt = font.render("Solved in " + str(elapsed_time) + "seconds", True,
                          GREEN)
        textRect = txt.get_rect(center=(299, 49))
        screen.blit(txt, textRect)
        pygame.display.update()

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
            if tile.x + xy_dist[0] == empty_x and \
                    tile.y + xy_dist[1] == empty_y:
                move_counter += 1
                empty_x = tile.x
                empty_y = tile.y
                tile.move_it(xy_dist)
                break

    screen.fill(BLACK, [200, 515, 200, 85])
    moves_display("Moves: " + str(move_counter))
    pygame.display.update()
    clock.tick(60)

    show_congrats()
    victory.play()
    time.sleep(3)
