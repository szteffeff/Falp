import pygame


def strip_from_sheet(sheet, start, size, columns, rows):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames


def get_level(level_id):
    return pygame.image.load(map_files[level_id][0]).convert()


def get_masks(level_id):
    mask_img = pygame.image.load(map_files[level_id][1]).convert_alpha()
    black_mask = pygame.mask.from_threshold(mask_img, (10, 10, 10, 255), (1, 1, 1, 255))
    red_mask = pygame.mask.from_threshold(mask_img, (127, 10, 10, 255), (127, 1, 1, 255))
    blue_mask = pygame.mask.from_threshold(mask_img, (0, 0, 127, 255))
    return [black_mask, red_mask, blue_mask]


def get_shadow():
    shadow = pygame.transform.scale(pygame.image.load("shadow.png"), (49, 20)).convert_alpha()
    return shadow


def get_player():
    boy = pygame.transform.scale(pygame.image.load("boy_idle.png"), animation_info["IDLE"][3]).convert_alpha()
    boy_rs = pygame.transform.scale(pygame.image.load("boy_run_south.png"), (animation_info["SOUTH"][3])).convert_alpha()
    boy_rl = pygame.transform.scale(pygame.image.load("boy_run_left.png"), (animation_info["WEST"][3])).convert_alpha()
    boy_rr = pygame.transform.flip(boy_rl, True, False)
    boy_rn = pygame.transform.scale(pygame.image.load("boy_run_south.png"), (animation_info["NORTH"][3])).convert_alpha()

    boy_idle = strip_from_sheet(boy, (0, 0), (48, 128), 1, 4)
    boy_run_south = strip_from_sheet(boy_rs, (0, 0), (128, 128), 1, 8)
    boy_run_west = strip_from_sheet(boy_rl, (0, 0), (128, 128), 1, 8)
    boy_run_east = strip_from_sheet(boy_rr, (0, 0), (128, 128), 1, 8)
    boy_run_north = strip_from_sheet(boy_rn, (0, 0), (128, 128), 1, 8)

    boy_animation = [boy_run_north, boy_run_south, boy_run_east, boy_run_west, boy_run_north, boy_run_north, boy_run_east,
                     boy_run_west, boy_idle]

    return boy_animation


def get_monster(varient):
    if varient == "SMALL_MUSHROOM":
        frames = strip_from_sheet(pygame.transform.scale(pygame.image.load("mini_mushroom.png"), (160, 64)), (0, 0), (32, 32), 5, 2)
        return [frames[0], frames[5]]


monster_info = {
    # "NAME": [IMAGE, SIZE, SPEED]
    "SMALL_MUSHROOM": ["mini_mushroom.png", (32, 32), 0.5, 10]
}

animation_info = {
    # "NAME": [ID, FRAME COUNT, SPEED, SIZE]
    "NORTH": [0, 8, 200, (128, 128 * 8)],
    "SOUTH": [1, 8, 60, (128, 128 * 8)],
    "EAST": [2, 8, 100, (128, 128 * 8)],
    "WEST": [3, 8, 100, (128, 128 * 8)],
    "NORTH_EAST": [4, 4, 200, (128, 128 * 8)],
    "NORTH_WEST": [5, 4, 200, (128, 128 * 8)],
    "SOUTH_EAST": [6, 8, 100, (128, 128 * 8)],
    "SOUTH_WEST": [7, 8, 100, (128, 128 * 8)],
    "IDLE": [8, 4, 200, (48, 128 * 4)]
}

map_files = {
    0: ["void.png", "empty.png"],

    1: ["test_map1.png", "mask1.png"],

    10: ["test_map1.png", "mask1.png"],
    11: ["test_map1.png", "mask1.png"],
    12: ["test_map1.png", "mask1.png"],
    13: ["test_map1.png", "mask1.png"],
    14: ["test_map1.png", "mask1.png"],
    15: ["test_map1.png", "mask1.png"],
    16: ["test_map1.png", "mask1.png"],

    20: ["test_map1.png", "mask1.png"],
    21: ["test_map1.png", "mask1.png"],
    22: ["test_map1.png", "mask1.png"],
    23: ["test_map1.png", "mask1.png"],
    24: ["test_map1.png", "mask1.png"],
    25: ["test_map1.png", "mask1.png"],
    26: ["test_map1.png", "mask1.png"],

    40: ["test_map1.png", "mask1.png"],
    41: ["test_map1.png", "mask1.png"],
    42: ["test_map1.png", "mask1.png"],
    43: ["test_map1.png", "mask1.png"],
    44: ["test_map1.png", "mask1.png"],
    45: ["test_map1.png", "mask1.png"],
    46: ["test_map1.png", "mask1.png"],

    50: ["test_map1.png", "mask1.png"],
    51: ["test_map1.png", "mask1.png"],
    52: ["test_map1.png", "mask1.png"],
    53: ["test_map1.png", "mask1.png"],
    54: ["test_map1.png", "mask1.png"],
    55: ["test_map1.png", "mask1.png"],
    56: ["test_map1.png", "mask1.png"],

    60: ["test_map1.png", "mask1.png"],
    61: ["test_map1.png", "mask1.png"],
    62: ["test_map1.png", "mask1.png"],
    63: ["test_map1.png", "mask1.png"],
    64: ["test_map1.png", "mask1.png"],
    65: ["test_map1.png", "mask1.png"],
    66: ["test_map1.png", "mask1.png"],

    70: ["test_map1.png", "mask1.png"],
    71: ["test_map1.png", "mask1.png"],
    72: ["test_map1.png", "mask1.png"],
    73: ["test_map1.png", "mask1.png"],
    74: ["test_map1.png", "mask1.png"],
    75: ["test_map1.png", "mask1.png"],
    76: ["test_map1.png", "mask1.png"],
}

#         Y 0  1  2  3  4  5  6  7  8  9
map_map = ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 1
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 2
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 3
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 4
           (0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # 5
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 6
           (0, 0, 0, 0, 0, 1, 0, 0, 0, 0),  # 7
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 8
           (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))  # 9
#                                             X
