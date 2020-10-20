import pygame
import time
import functions
import player
import stage
import monster
import user_interface
import cProfile

FRAMERATE = 100
FULLSCREEN = False

delta = 0
changed_pixels = []

pygame.init()

screen_size = functions.get_scale(functions.resize())[0]


def flags():
    if FULLSCREEN:
        display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
    else:
        display_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
    return display_flags


screen = pygame.display.set_mode(screen_size, flags())

screen.set_alpha(None)  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # THIS MIGHT BE THE PROBLEM

run = True

clock = pygame.time.Clock()

boy = player.Player()
level = stage.Stage()
monster = monster.Monster((960, 540), "SMALL_MUSHROOM")
menu = user_interface.Menu()

move = pygame.event.custom_type()

pygame.time.set_timer(move, 1556)

frame = pygame.Surface((1920, 1080))

frame_size = functions.get_scale(screen_size)


def dialog_box(position, size):
    global delta
    delta = 0
    frame.blits(menu.dialog(position, size), False)
    render_frame(True)
    while True:
        if pygame.mouse.get_pressed()[0]:
            break
        print(pygame.mouse.get_pressed())

def render_frame(refresh):
    if frame_size[0] != [1920, 1080] or refresh:
        full_frame = pygame.transform.scale(frame, frame_size[0])
        screen.blit(full_frame, frame_size[1])
        pygame.display.update()
    else:  # SUPER SPEED ACTIVATE
        for rect in changed_pixels:
            rect.move_ip(0, frame_size[1][1])
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
        delta = clock.tick(FRAMERATE) / 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
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
            level.switch(boy.move(delta, level.masks))
        else:
            boy.moving = [False, "IDLE", boy.moving[2]]

        if keys[pygame.K_u]:
            pygame.display.update()
            print(frame_size[1])

        if keys[pygame.K_p]:
            time.sleep(1)

        if keys[pygame.K_t]:
            boy.speed = float(input("SPEED"))

        if keys[pygame.K_b]:
            dialog_box([960, 540], 5)

        every = [level.blit(), monster.blit(), boy.blit(delta)[0], boy.blit(delta)[1]]

        changed_pixels.append(frame.blits(every, True)[0])

        render_frame(False)
        if level.new_frame > 0:
            render_frame(True)
            level.new_frame -= 1

        pygame.display.set_caption(f"RESOLUTION:{frame_size[0]} | STAGE-ID:{level.id} | OVERMAP:{list(reversed(level.over_map))} POSITION:{boy.position} | {round(clock.get_fps())} FPS")


cProfile.run('main()')

main()
