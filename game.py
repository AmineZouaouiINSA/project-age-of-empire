import pygame
import sys
from definitions import *
from world import World
from camera import Camera


from selection_fonction import Selection
from hud import *
from worker import *
from IA import *
####VARIABLES GLOBALES


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.entities = [] #Les unités



        # hud
        self.hud = Hud(self.width, self.height)
        #World
        self.world = World(self.entities,self.hud,MAP_SIZE,MAP_SIZE,self.width,self.height)

        #Camera
        self.camera = Camera(self.width, self.height)

        # Selecteur
        self.selecteur = Selection(self.screen)

        Archer(self.world.world[4][3], self.world, self.camera,"player")
        #Axemen(self.world.world[9][10], self.world, self.camera,"enemy")
        ScoutShip(self.world.world[25][2], self.world, self.camera,"player")
        Villageois(self.world.world[5][3], self.world, self.camera,"player")
        Clubman(self.world.world[4][6], self.world, self.camera,"enemy")
        Scout(self.world.world[5][15], self.world, self.camera,"player")

        #######################IA
        #ArcherIA(self.world.world[35][35],self.world,self.camera)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def events(self):
        for event in pygame.event.get(): # Si on clique sur la croix pour quitter, on arrete le jeu
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()




    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)
        for e in self.entities :
            e.update_animation(0.2)
            e.update()






    def draw(self): #Construction graphiques
        self.screen.fill(BLACK)  # Arrière plan
        self.world.draw(self.screen,self.camera)
        self.hud.draw(self.screen)
        pygame.display.flip()

