import definitions


# import functions

class Stage:
    STARTING_LEVEL = 1

    def __init__(self):
        self.image_main = definitions.get_level(self.STARTING_LEVEL)
        self.masks = definitions.get_masks(self.STARTING_LEVEL)
        self.id = 1
        self.over_map = [7, 5]
        self.new_frame = 0

    def blit(self):
        return [self.image_main, (0, 0)]

    def switch(self, direction):
        if direction == "UP":
            self.over_map[0] = (self.over_map[0] - 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)

        elif direction == "DOWN":
            self.over_map[0] = (self.over_map[0] + 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)

        elif direction == "LEFT":
            print("left")
            self.over_map[1] = (self.over_map[1] - 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)

        elif direction == "RIGHT":
            print("RIGHT")
            self.over_map[1] = (self.over_map[1] + 1) % 10
            self.id = definitions.map_map[self.over_map[0]][self.over_map[1]]
            self.image_main = definitions.get_level(self.id)
            self.masks = definitions.get_masks(self.id)

        self.new_frame = 100
