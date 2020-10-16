import definitions
import random
import pygame


class Monster:
    def __init__(self, origin, variant):
        self.position = origin
        self.alive = True
        self.path = None
        self.movement = 0
        if variant == "SMALL_MUSHROOM":
            self.frames = [0, 1]
            self.animation = definitions.get_monster("SMALL_MUSHROOM")
            self.size = definitions.monster_info["SMALL_MUSHROOM"][1]
            self.update_rect = pygame.Rect(0, 0, 48, 48)
            self.speed = (definitions.monster_info["SMALL_MUSHROOM"][2] * (random.uniform(0.5, 1.5)))
            self.health = definitions.monster_info["SMALL_MUSHROOM"][3]

    def blit(self):
        if self.frames[0] > self.frames[1]:
            self.frames[0] = 0

        self.frames[0] += 0.01

        return self.animation[round(self.frames[0])], (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2)

    def pathfind(self, target):
        pass

    def die(self):
        pass

    def live(self):
        self.blit()
        self.pathfind((0, 0))
        if self.health <= 0:
            self.die()
