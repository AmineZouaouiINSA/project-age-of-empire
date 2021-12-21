import pygame
from Mouvement import *
import math

class Block():
    def __init__(self):
        self.max = 300  # Point de vie max
        self.vie = 180  # Point de vie actuel
        self.width = 50 #largeur du block
        self.height = 100 #hauteur du block

        self.img = pygame.Surface([self.width,self.height])
        self.img.fill((0,255,0))
        self.pos_x = 300
        self.pos_y = 300

        self.posDepart = [self.pos_x, self.pos_y]
        self.posArrivee = [200, 400]
        self.progression = 0
        self.speed = 2


    def draw(self):
        screen.blit(self.img, (self.pos_x - (self.width/2),self.pos_y - (self.height)))

    def update(self):
        distance = math.sqrt( (self.posArrivee[0]-self.posDepart[0])*(self.posArrivee[0]-self.posDepart[0]) + (self.posArrivee[1]-self.posDepart[1])*(self.posArrivee[1]-self.posDepart[1]) )
        if distance != 0:
            dt = 1 / distance
            if self.progression < 1:
                self.progression += self.speed * dt
            else:
                self.progression = 1
            self.pos_x = lerp(self.posDepart[0], self.posArrivee[0], self.progression)
            self.pos_y = lerp(self.posDepart[1], self.posArrivee[1], self.progression)


    def pos_darrivee(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            self.posArrivee[0], self.posArrivee[1] = mx, my
            self.posDepart[0], self.posDepart[1] = (self.pos_x, self.pos_y)
            self.progression = 0
            self.update()

    def draw_BarreVie(self):
        ratio = self.vie/self.max #ratio d'HP
        barreBlanche = pygame.Surface([self.width/2,5])
        barreBlanche.fill((255,255,255))
        barreRouge = pygame.Surface([ratio*(self.width/2),5])
        barreRouge.fill((255,0,0))
        screen.blit(barreBlanche, (self.pos_x - (self.width/4), self.pos_y - (self.height +10)))
        screen.blit(barreRouge, (self.pos_x - (self.width / 4), self.pos_y - (self.height + 10)))



pygame.init()

# affiche la fenêtre
screen = pygame.display.set_mode((600, 600))

#initialise un block
block = Block()

############# BOUCLE DE JEU ##########
continuer = True
clock = pygame.time.Clock()
running = True
while running :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

#######################################

    # AFFICHE ECRAN
    screen.fill((0,0,0))

    ######## AFFICHE ET UPDATE BLOCK ########
    block.pos_darrivee()
    block.update()
    block.draw()
    block.draw_BarreVie()

    #########################################


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
quit()
