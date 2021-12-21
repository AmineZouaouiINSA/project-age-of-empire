import pygame, sys, random
from definitions import *
#from Personnage2 import *

class Selection(pygame.sprite.Sprite):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.draw_new_selection_box = False
        self.selection_completed = False
        self.selected_units = []
        self.leftclick_down_location = {'' for e in range(2)}
        self.leftclick_up_location = {'' for e in range(2)}
        self.current_mouse_location = pygame.mouse.get_pos()
        self.rect = []
        self.nb_click = 0

    def create_box(self,p1, p2):
        x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
        x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
        return pygame.Rect(x1, y1, x2 - x1, y2 - y1)

    def select(self):
        if self.draw_new_selection_box:
            self.selection_box = self.create_box(self.leftclick_down_location, pygame.mouse.get_pos())
        elif self.selection_completed:
            self.completed_selection_box = self.create_box(self.leftclick_down_location, self.leftclick_up_location)

        '''for unit in units:
            if self.draw_new_selection_box:
                pygame.draw.rect(self.window, (255, 0, 0), self.selection_box, 2)
                for unit in units:
                    if self.selection_box.colliderect(unit.rect):
                        pygame.draw.rect(self.window, (0, 0, 255), unit, 2)
            if self.selection_completed:
                selected_units = []
                for unit in units:
                    if self.completed_selection_box.colliderect(unit.rect):
                        pygame.draw.rect(self.window, (0, 0, 255), unit, 2)
                        unit.selected = True
                    else:
                        unit.selected = False'''

    def eventSelecteur_letftdown(self):
        #Archer1.selection()
        self.leftclick_down_location = pygame.mouse.get_pos()
        self.selected_units = False
        self.draw_new_selection_box = True

    def eventSelecteur_leftup(self):
        self.leftclick_up_location = pygame.mouse.get_pos()
        self.draw_new_selection_box = False
        self.selection_completed = True

