import pygame


def get_scale(screen):  # used for resizing and centering screen
    dim = 0
    centered = [0, 0]
    while (dim + 1) * 16 <= screen[0]:
        dim += 1

    while not (dim * 9) <= screen[1]:
        dim -= 1

    if screen[0] is not dim * 16:
        centered[0] = int((screen[0] - dim * 16) / 2)
    if screen[1] is not dim * 9:
        centered[1] = int((screen[1] - dim * 9) / 2)

    return [[dim * 16, dim * 9], [centered[0], centered[1]]]


def resize():
    display = pygame.display.Info()
    if display.current_w < display.current_h:
        size = display.current_w
    else:
        size = display.current_h
    return [int(size), int(size)]


def rect_check(start, movement, rect_size, direction, masks):
    bounding_box = pygame.Surface((rect_size[0], rect_size[1]))
    bounding_mask = pygame.mask.from_surface(bounding_box)
    bounding_mask.fill()

    main_mask = masks[0]

    if not direction:
        return bounding_mask

    new_pos = start
    # print(f"{movement}-")
    # if masks[1].overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(start[1] - 1 - rect_size[1] / 2))):
    #     movement[0] = round(movement[0] / 2)
    #     movement[1] = round(movement[1] / 2)
    #
    # print(movement)

    if direction is "NORTH":
        to_move = abs(movement[1])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] - 1 - rect_size[1] / 2))):
                new_pos[1] -= 1
        return new_pos

    elif direction is "SOUTH":
        to_move = abs(movement[1])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] + 1 - rect_size[1] / 2))):
                new_pos[1] += 1
        return new_pos

    elif direction is "EAST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] + 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] += 1
        return new_pos

    elif direction is "WEST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] - 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] -= 1
        return new_pos

    elif direction is "NORTH_EAST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] - 1 - rect_size[1] / 2))):
                new_pos[1] -= 1
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] + 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] += 1
        return new_pos

    elif direction is "NORTH_WEST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] - 1 - rect_size[1] / 2))):
                new_pos[1] -= 1
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] - 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] -= 1
        return new_pos

    elif direction is "SOUTH_EAST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] + 1 - rect_size[1] / 2))):
                new_pos[1] += 1
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] + 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] += 1
        return new_pos

    elif direction is "SOUTH_WEST":
        to_move = abs(movement[0])
        for move in range(to_move):
            if not main_mask.overlap(bounding_mask, (int(start[0] - rect_size[0] / 2), int(new_pos[1] + 1 - rect_size[1] / 2))):
                new_pos[1] += 1
            if not main_mask.overlap(bounding_mask, (int(new_pos[0] - 1 - rect_size[0] / 2), int(start[1] - rect_size[1] / 2))):
                new_pos[0] -= 1
        return new_pos

    print("Nosotras tenemos un gran problema")

    return start


def get_line(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
