import definitions
import pygame
import functions


class Player:
    RESOLUTION = (128, 128)

    def __init__(self):
        self.position = [1920 / 2, 1080 / 2]  # x, y
        self.moving = [False, "SOUTH", 0, 0]  # is moving, direction, frame of animation
        self.animations = definitions.get_player()
        self.movement = [0, 0]
        self.shadow = definitions.get_shadow()
        self.dot = pygame.image.load("dot.png")
        self.update_rect = pygame.Rect(0, 0, 128, 148)
        self.collision_size = [44, 24]
        self.speed = 0.4
        self.surface = pygame.Surface((148, 148))

    def move(self, delta, masks):
        self.movement = [0, 0]
        if self.moving[0]:
            if self.moving[1] in ["NORTH", "NORTH_EAST", "NORTH_WEST"]:
                self.movement[1] -= 1 * delta * self.speed
            if self.moving[1] in ["SOUTH", "SOUTH_EAST", "SOUTH_WEST"]:
                self.movement[1] += 1 * delta * self.speed
            if self.moving[1] in ["EAST", "NORTH_EAST", "SOUTH_EAST"]:
                self.movement[0] += 1 * delta * self.speed
            if self.moving[1] in ["WEST", "NORTH_WEST", "SOUTH_WEST"]:
                self.movement[0] -= 1 * delta * self.speed

            if self.moving[1] in ["NORTH_WEST", "SOUTH_WEST", "NORTH_EAST", "SOUTH_EAST"]:
                xy_avg = round(abs(self.movement[0]) + abs(self.movement[1]) / 2)
                self.movement[0] = xy_avg * (self.movement[0] / abs(self.movement[0])) / 2
                self.movement[1] = xy_avg * (self.movement[1] / abs(self.movement[1])) / 2

            self.movement[0] = round(self.movement[0])
            self.movement[1] = round(self.movement[1])

            self.position = functions.rect_check(self.position, self.movement, self.collision_size, self.moving[1], masks)

            if 0 >= self.position[0] or self.position[0] >= 1920:
                if 0 >= self.position[0]:
                    self.position[0] += 1920
                    return "LEFT"
                else:
                    self.position[0] -= 1920
                    return "RIGHT"
            elif 0 >= self.position[1] or self.position[1] >= 1080:
                if 0 >= self.position[1]:
                    self.position[1] += 1080
                    return "UP"
                else:
                    self.position[1] -= 1080
                    return "DOWN"
        return None

    def blit(self, delta):

        if self.moving[2] >= definitions.animation_info[self.moving[1]][1] - 1:
            # Do not exceed number of frames in animation
            self.moving[2] = 0

        self.moving[2] += 1 / definitions.animation_info[self.moving[1]][2] * delta  # increment frame of animation accordion to delta and speed defined in dictionary

        return (self.shadow, (self.position[0] - 22 - 1, self.position[1] - 9)), (self.animations[definitions.animation_info[self.moving[1]][0]][round(self.moving[2])], (self.position[0] - (definitions.animation_info[self.moving[1]][3][0] / 2 - 1), (self.position[1] - self.RESOLUTION[1] + 9)))

    def live(self):
        pass
