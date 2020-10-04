import pygame
import time
# import math
import definitions
import functions

FRAMERATE = 100
FULLSCREEN = False

delta = 0
changed_pixels = []

pygame.init()

screen_size = functions.get_scale(functions.resize())[0]


def flags():
    # display = pygame.display.Info()
    if FULLSCREEN:
        display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
    else:
        display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
    return display_flags


screen = pygame.display.set_mode(screen_size, flags())

screen.set_alpha(None)  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # THIS MIGHT BE THE PROBLEM


class Player:
    RESOLUTION = (128, 128)

    def __init__(self):
        self.position = [1920 / 2, 1080 / 2]  # x, y
        self.moving = [False, "SOUTH", 0, 0]  # is moving, direction, frame of animation
        self.animations = definitions.get_player()
        self.movement = [0, 0]
        self.shadow = definitions.get_shadow()
        self.dot = pygame.image.load("dot.png")
        self.update_rect = pygame.Rect(0, 0, 160, 160)
        self.collision_size = [44, 24]

    def move(self, test):
        self.movement = [0, 0]
        if self.moving[0] or test:
            if self.moving[1] in ["NORTH", "NORTH_EAST", "NORTH_WEST"]:
                self.movement[1] -= 1 * delta / 4
            if self.moving[1] in ["SOUTH", "SOUTH_EAST", "SOUTH_WEST"]:
                self.movement[1] += 1 * delta / 4
            if self.moving[1] in ["EAST", "NORTH_EAST", "SOUTH_EAST"]:
                self.movement[0] += 1 * delta / 4
            if self.moving[1] in ["WEST", "NORTH_WEST", "SOUTH_WEST"]:
                self.movement[0] -= 1 * delta / 4

            if self.moving[1] in ["NORTH_WEST", "SOUTH_WEST", "NORTH_EAST", "SOUTH_EAST"]:
                xy_avg = round(abs(self.movement[0]) + abs(self.movement[1]) / 2)
                self.movement[0] = xy_avg * (self.movement[0] / abs(self.movement[0])) / 2
                self.movement[1] = xy_avg * (self.movement[1] / abs(self.movement[1])) / 2

            self.movement[0] = round(self.movement[0])
            self.movement[1] = round(self.movement[1])

            if test:
                self.movement[0] = int(input("PLAN:"))
                self.movement[1] = int(input("PLAN1:"))
                self.moving[1] = input("DIR:")

            self.position = functions.rect_check(self.position, self.movement, self.collision_size, self.moving[1], level.masks[0])

            if 0 >= self.position[0] or self.position[0] >= 1920:
                if 0 >= self.position[0]:
                    print("RIGHT")
                else:
                    print("LEFT")
            elif 0 >= self.position[1] or self.position[1] >= 1080:
                if 0 >= self.position[1]:
                    print("UP")
                else:
                    print("DOWN")

    def blit(self):

        frame.blit(self.shadow, (self.position[0] - 22 - 1, self.position[1] - 9))
        # Draw shadow | shadow.png = 26 , 12

        if self.moving[2] >= definitions.animation_info[self.moving[1]][1] - 1:
            # Do not exceed number of frames in animation
            self.moving[2] = 0

        frame.blit(self.animations[definitions.animation_info[self.moving[1]][0]][round(self.moving[2])], (
            self.position[0] - (definitions.animation_info[self.moving[1]][3][0] / 2 - 1),
            (self.position[1] - self.RESOLUTION[1] + 9)))

        self.moving[2] += 1 / definitions.animation_info[self.moving[1]][
            2] * delta  # increment frame of animation accordion to delta and speed defined in dictionary

        frame.blit(self.dot, (self.position[0], self.position[1] - 1))

        changed_pixels.append(self.update_rect.move(self.position[0] - 80 + 1, self.position[1] - 80 + 9))


class Stage:
    STARTING_LEVEL = 00

    def __init__(self):
        self.image_main = definitions.get_level(self.STARTING_LEVEL)
        self.masks = definitions.get_masks(self.STARTING_LEVEL)
        self.id = 00

    def blit(self):
        frame.blit(self.image_main, (0, 0))

    def switch(self, direction):
        pass


class Monster:
    def __init__(self, origin, variant):
        self.position = origin
        if variant == "SMALL_MUSHROOM":
            self.frames = [0, 1]
            self.animation = definitions.get_monster("SMALL_MUSHROOM")
            self.size = definitions.monster_info["SMALL_MUSHROOM"][1]
            self.update_rect = pygame.Rect(0, 0, 64, 64)

    def blit(self):
        if self.frames[0] > self.frames[1]:
            self.frames[0] = 0

        frame.blit(self.animation[round(self.frames[0])], (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2))

        changed_pixels.append(self.update_rect.move(self.position[0] - 32, self.position[1] - 32))

        self.frames[0] += 0.01


run = True

clock = pygame.time.Clock()

boy = Player()
level = Stage()
shroom = Monster((960, 540), "SMALL_MUSHROOM")

frame = pygame.Surface((1920, 1080))

# function optimizations
frame_size = functions.get_scale(screen_size)


def render_frame():
    if frame_size[0] != [1920, 1080]:
        full_frame = pygame.transform.scale(frame, frame_size[0])
        screen.blit(full_frame, frame_size[1])
        pygame.display.update()
    else:  # SUPER SPEED ACTIVATE
        screen.blit(frame, frame_size[1])
        pygame.display.update(changed_pixels)


while run:
    changed_pixels = []
    delta = clock.tick(FRAMERATE)
    delta2 = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, flags())
            screen_size = event.size
            frame_size = functions.get_scale(screen_size)
            render_frame()
            pygame.display.update()

    keys = pygame.key.get_pressed()

    level.blit()

    # level.masks[0].to_surface(frame)

    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
        if keys[pygame.K_w] and not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_s]):
            boy.moving = [True, "NORTH", boy.moving[2]]
        elif keys[pygame.K_a] and not (keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s]):
            boy.moving = [True, "WEST", boy.moving[2]]
        elif keys[pygame.K_s] and not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d]):
            boy.moving = [True, "SOUTH", boy.moving[2]]
        elif keys[pygame.K_d] and not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a]):
            boy.moving = [True, "EAST", boy.moving[2]]
        elif keys[pygame.K_w] and keys[pygame.K_d] and not (keys[pygame.K_s] or keys[pygame.K_a]):
            boy.moving = [True, "NORTH_EAST", boy.moving[2]]
        elif keys[pygame.K_w] and keys[pygame.K_a] and not (keys[pygame.K_s] or keys[pygame.K_d]):
            boy.moving = [True, "NORTH_WEST", boy.moving[2]]
        elif keys[pygame.K_s] and keys[pygame.K_d] and not (keys[pygame.K_w] or keys[pygame.K_a]):
            boy.moving = [True, "SOUTH_EAST", boy.moving[2]]
        elif keys[pygame.K_s] and keys[pygame.K_a] and not (keys[pygame.K_w] or keys[pygame.K_d]):
            boy.moving = [True, "SOUTH_WEST", boy.moving[2]]
        boy.move(False)
    else:
        boy.moving = [False, "IDLE", boy.moving[2]]

    if keys[pygame.K_u]:
        pygame.display.update()

    if keys[pygame.K_p]:
        time.sleep(1)

    if keys[pygame.K_t]:
        boy.move(True)

    if keys[pygame.K_i]:
        print(boy.position)

    boy.blit()
    shroom.blit()

    render_frame()

pygame.quit()
