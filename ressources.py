from pathlib import Path
from random import randint
import pygame


class Arbre(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y) :
        super().__init__()

        self.type_perso = "Arbre"
        self.health = 300
        self.image = pygame.image.load(Path('Textures/Tree.gif'))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x #randint(1,1080)
        self.rect.y = pos_y #randint(1,800)
        
class Mine_or(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()

        self.type_perso = "Mine d'or"
        self.health = 300
        self.img = pygame.image.load("")
        self.rect = self.img.get_rect()
        self.rect.x = randint(1, 1080)
        self.rect.y = randint(1, 800)

class Mine_de_pierre(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()

        self.type_perso = "Mine de pierre"
        self.health = 300
        self.img = pygame.image.load("")
        self.rect = self.img.get_rect()
        self.rect.x = randint(1, 1080)
        self.rect.y = randint(1, 800)

class Arbre_baie(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()

        self.type_perso = "Arbre à baie"
        self.health = 100000000000
        self.img = pygame.image.load("")
        self.rect = self.img.get_rect()
        self.rect.x = randint(1, 1080)
        self.rect.y = randint(1, 800)
         