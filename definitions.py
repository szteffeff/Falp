import pygame


def strip_from_sheet(sheet, start, size, columns, rows):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames


def get_level(level_id):
    stage = pygame.image.load(map_files[level_id][0]).convert()
    return stage


def get_masks(level_id):
    mask_img = pygame.image.load(map_files[level_id][1]).convert_alpha()
    black_mask = pygame.mask.from_surface(mask_img)
    red_mask = pygame.mask.from_threshold(mask_img, (255, 0, 0))
    blue_mask = pygame.mask.from_threshold(mask_img, (0, 0, 255))
    return [black_mask, red_mask, blue_mask]


def get_shadow():
    shadow = pygame.transform.scale(pygame.image.load("shadow.png"), (49, 20)).convert_alpha()
    return shadow


def get_player():
    boy = pygame.transform.scale(pygame.image.load("boy_idle.png"), animation_info["IDLE"][3]).convert_alpha()
    boy_rs = pygame.transform.scale(pygame.image.load("boy_run_south.png"), (animation_info["SOUTH"][3])).convert_alpha()
    boy_idle = strip_from_sheet(boy, (0, 0), (48, 128), 1, 4)
    boy_run_south = strip_from_sheet(boy_rs, (0, 0), (128, 128), 1, 8)
    boy_animation = [boy_idle, boy_run_south, boy_idle, boy_idle, boy_idle, boy_idle, boy_run_south,
                     boy_run_south, boy_idle]

    return boy_animation


def get_monster(varient):
    if varient == "SMALL_MUSHROOM":
        frames = strip_from_sheet(pygame.transform.scale(pygame.image.load("mini_mushroom.png"), (320, 128)), (0, 0), (64, 64), 5, 2)
        return [frames[0], frames[5]]


monster_info = {
    "SMALL_MUSHROOM": ["mini_mushroom.png", (64, 64)]
}

animation_info = {
    # "NAME": [ID, FRAME COUNT, SPEED, SIZE]
    "NORTH": [0, 4, 200, (48, 128 * 4)],
    "SOUTH": [1, 8, 60, (128, 128 * 8)],
    "EAST": [2, 4, 200, (48, 128 * 4)],
    "WEST": [3, 4, 200, (48, 128 * 4)],
    "NORTH_EAST": [4, 4, 200, (48, 128 * 4)],
    "NORTH_WEST": [5, 4, 200, (48, 128 * 4)],
    "SOUTH_EAST": [6, 8, 60, (128, 128 * 4)],
    "SOUTH_WEST": [7, 8, 60, (128, 128 * 4)],
    "IDLE": [8, 4, 200, (48, 128 * 4)]
}

map_files = {
    00: ["test_map1.png", "test_mask.png"]

}

map_move = {
    "UP": 10
}
