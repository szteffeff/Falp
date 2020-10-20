import definitions
import pygame


class Menu:

    def __init__(self):
        self.piece_right = definitions.get_menu()[2]
        self.piece_center = definitions.get_menu()[1]
        self.piece_left = definitions.get_menu()[0]

    def mainMenu(self):
        pass

    def dialog(self, location, size):

        box = pygame.Surface((int(32 * size), 32))
        for i in range(size):
            if i == 0:
                box.blit(self.piece_left, (0, 0))
            elif i == (size - 1):
                box.blit(self.piece_right, (32 * (size - 1), 0))
            else:
                print("center")
                box.blit(self.piece_center, (32 * (size - 1), 0))

        return [[box, location]]
