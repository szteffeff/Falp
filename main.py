import pygame
import time
import random
import definitions
import functions
import cProfile

FRAMERATE = 1000
FULLSCREEN = False

delta = 0
changed_pixels = []

pygame.init()

screen_size = functions.get_scale(functions.resize())[0]


def flags():
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
        self.update_rect = pygame.Rect(0, 0, 128, 148)
        self.collision_size = [44, 24]
        self.speed = 0.4

    def move(self, test):
        self.movement = [0, 0]
        if self.moving[0] or test:
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

            if test:
                self.movement[0] = int(input("PLAN:"))
                self.movement[1] = int(input("PLAN1:"))
                self.moving[1] = input("DIR:")

            self.position = functions.rect_check(self.position, self.movement, self.collision_size, self.moving[1], level.masks)

            if 0 >= self.position[0] or self.position[0] >= 1920:
                if 0 >= self.position[0]:
                    level.switch("LEFT")
                else:
                    level.switch("RIGHT")
            elif 0 >= self.position[1] or self.position[1] >= 1080:
                if 0 >= self.position[1]:
                    level.switch("UP")
                else:
                    level.switch("DOWN")

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

        changed_pixels.append(self.update_rect.move(self.position[0] - (definitions.animation_info[self.moving[1]][3][0] / 2 - 1), self.position[1] - self.RESOLUTION[1] + 9 + frame_size[1][1]))

    def live(self):
        self.blit()


class Stage:
    STARTING_LEVEL = 1

    def __init__(self):
        self.image_main = definitions.get_level(self.STARTING_LEVEL)
        self.masks = definitions.get_masks(self.STARTING_LEVEL)
        self.id = 1
        self.over_map = [7, 5]
        self.new_frame = 0

    def blit(self):
        frame.blit(self.image_main, (0, 0))

    def switch(self, direction):
        monsters.clear()
        monsters.append(boy)
        if direction == "UP":
            self.over_map[0] = (self.over_map[0] - 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)
            boy.position[1] += 1080

        elif direction == "DOWN":
            self.over_map[0] = (self.over_map[0] + 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)
            boy.position[1] -= 1080

        elif direction == "LEFT":
            print("left")
            self.over_map[1] = (self.over_map[1] - 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)
            boy.position[0] += 1920

        elif direction == "RIGHT":
            print("RIGHT")
            self.over_map[1] = (self.over_map[1] + 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)
            boy.position[0] -= 1920

        level.blit()
        self.new_frame = 100
        render_frame(True)


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

        frame.blit(self.animation[round(self.frames[0])], (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2))

        frame.blit(boy.dot, (self.position[0], self.position[1]))

        changed_pixels.append(self.update_rect.move(self.position[0] - 24, self.position[1] - 24 + frame_size[1][1]))

        self.frames[0] += 0.01

    def pathfind(self, target):

        if not self.path:
            path_to_target = functions.get_line(self.position, [round(target[0]), round(target[1])])

            for pos in path_to_target:
                if level.masks[0].get_at(pos):
                    self.path = functions.get_line(self.position, (round(random.random() * 1919), round(random.random() * 1079)))
                    for index, pos2 in enumerate(self.path):
                        if level.masks[0].get_at(pos2):
                            del self.path[:index]
                            break
                else:
                    self.path = path_to_target
        else:
            if self.movement >= 100:
                self.position = self.path[0]
                self.movement = 0
                del self.path[0]
            self.movement += 10 * delta * self.speed

    def die(self):
        pass

    def live(self):
        self.blit()
        self.pathfind(boy.position)
        if self.health <= 0:
            self.die()


run = True

clock = pygame.time.Clock()

boy = Player()
level = Stage()
monsters = [boy]

for i in range(1):
    monsters.append(Monster([960, 540], "SMALL_MUSHROOM"))

move = pygame.event.custom_type()

pygame.time.set_timer(move, 1556)

frame = pygame.Surface((1920, 1080))

frame_size = functions.get_scale(screen_size)


def render_frame(refresh):
    if frame_size[0] != [1920, 1080] or refresh:
        full_frame = pygame.transform.scale(frame, frame_size[0])
        screen.blit(full_frame, frame_size[1])
        pygame.display.update()
    else:  # SUPER SPEED ACTIVATE
        screen.blit(frame, frame_size[1])
        pygame.display.update(changed_pixels)


def main():
    global run
    global delta
    global changed_pixels
    global screen
    global screen_size
    global frame_size

    while run:
        changed_pixels = []
        delta = clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, flags())
                screen_size = event.size
                frame_size = functions.get_scale(screen_size)
                render_frame(True)
                pygame.display.update()
            if event.type == move:
                pass

        keys = pygame.key.get_pressed()

        level.blit()

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
            print(frame_size[1])

        if keys[pygame.K_p]:
            time.sleep(1)

        if keys[pygame.K_t]:
            boy.speed = float(input("SPEED"))

        if keys[pygame.K_i]:
            print(boy.position)

        for mon in monsters:
            mon.live()

        render_frame(False)
        if level.new_frame > 0:
            render_frame(True)
            level.new_frame -= 1

        pygame.display.set_caption(f"RESOLUTION:{frame_size[0]} | STAGE-ID:{level.id} | OVERMAP:{list(reversed(level.over_map))} POSITION:{boy.position} | {round(clock.get_fps())} FPS")


cProfile.run('main()')

pygame.quit()
