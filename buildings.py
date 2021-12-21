
import pygame

class towncenter:

    def __init__(self, pos, team):
        self.image = pygame.image.load("assets/Towncenter.png")
        self.name = "towncenter"
        self.rect = self.image.get_rect(topleft=pos)
        self.counter = 0
        self.team = team

    def update(self):
        self.counter += 1

    def update_animation(self,speed):
        pass

class maison:

    def __init__(self, pos, team):
        self.image = pygame.image.load("Buildings/House1.png")
        self.name = "maison"
        self.rect = self.image.get_rect(topleft=pos)
        self.counter = 0
        self.team = team

    def update(self):
        self.counter += 1


    def update_animation(self,speed):
        pass