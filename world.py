
import pygame
import random
from Ressource import Ressource
from Tile import Tile
from definitions import *
from map import randomMap
from map import *
from random import randint
from buildings import *
#import noise
from worker import *
from IA import *

class World:
    def __init__(self,entities,hud,grid_length_x,grid_length_y,width,height):
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x  #Taille MAP
        self.grid_length_y = grid_length_y
        self.width = width  #Taille écran
        self.height = height
        self.perlin_scale = grid_length_x/5
        self.array_tiles = randomMap()
        self.map_tiles = pygame.Surface((grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world(self.array_tiles)

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.selected_units = []

        self.iaworkers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]


        self.temp_tile = None
        self.examine_tile = None
        self.collision_matrix = self.create_collision_matrix()
        
    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0

        return collision_matrix




    def update(self, camera):

        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()
        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        self.temp_tile = None
        # gridpos0 < 100 et gridpos1 < 100
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:
                    if self.hud.selected_tile["name"] == "Towncenter":
                        ent = towncenter(render_pos,"player")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "House":
                        ent = maison(render_pos,"player")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.world[grid_pos[0]][grid_pos[1]]["entity"] = True
                    self.hud.selected_tile = None

        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                building = self.buildings[grid_pos[0]][grid_pos[1]]
                if mouse_action[0] and (building is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building

    def draw(self, screen, camera):
        screen.blit(self.map_tiles, (camera.scroll.x, camera.scroll.y))
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos =  self.world[x][y]["render_pos"]
                #World Tiles
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                    (render_pos[0] + self.map_tiles.get_width()/2 + camera.scroll.x,
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))


                #draw worker
                worker = self.workers[x][y]
                if worker is not None :
                    if worker.team != "enemy" :
                        if worker.selected: pygame.draw.polygon(screen, (255, 255, 255), worker.iso_poly, 2)
                        screen.blit(worker.image, (
                            worker.pos_x + self.map_tiles.get_width() / 2 + camera.scroll.x + 45,
                            worker.pos_y - worker.image.get_height() + camera.scroll.y + 50))
                    else :
                        pygame.draw.polygon(screen, (255, 0, 0), worker.iso_poly, 2)
                        if worker.selected: pygame.draw.polygon(screen, (255, 255, 255), worker.iso_poly, 2)
                        screen.blit(worker.image, (
                            worker.pos_x + self.map_tiles.get_width() / 2 + camera.scroll.x + 45,
                            worker.pos_y - worker.image.get_height() + camera.scroll.y + 50))

                # draw IAworker
                iaworker = self.iaworkers[x][y]
                if iaworker is not None:
                    pygame.draw.polygon(screen, (255, 0, 0), iaworker.iso_poly, 2)
                    screen.blit(iaworker.image,
                                (render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x,
                                render_pos[1] - (iaworker.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    # Buildings tiles
                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image,
                                    (render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.map_tiles.get_width() / 2 + camera.scroll.x,
                                         y + render_pos[1] - (
                                                     building.image.get_height() - TILE_SIZE) + camera.scroll.y) for
                                        x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.map_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pygame.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.map_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self,array_tiles):
        world = []
        for grid_x in range(self.grid_length_x): #On itère pour la taille de la map
            world.append([])                     #On fait une liste avec chaque indice
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x,grid_y)
                world[grid_x].append(world_tile)
                render_pos = world_tile["render_pos"] #Position de rendu pour coller les cases ensembles
                self.map_tiles.blit(self.tiles[array_tiles[grid_x,grid_y]],(render_pos[0] + (self.map_tiles.get_width())/2 ,render_pos[1] ))
        return world    


    def grid_to_world(self, grid_x, grid_y):    #Renvoie un dictionnaire avec notamment des coordonnées isométriques pour une vue 2.5D
        rien = Ressource(0,"")
        tile1 = Tile(grid_x,grid_y,0, rien ,0)
        #Matrice avec coordonées cartésiennes
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)

        ]
        
        iso_poly = [self.cart_to_iso(x,y) for x,y in rect]
        minx = min([x for x,y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 500)
        perlin = 5 #* noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)

        if grid_y > 3:
            if ((perlin >= 15) or (perlin <= -35)) and self.array_tiles[grid_x,grid_y] != "water" and self.array_tiles[grid_x-1,grid_y-1] != "water" and self.array_tiles[grid_x-2,grid_y-2] != "water" :
                tile1 = "tree"
            else:
                if 1<r<10 and self.array_tiles[grid_x,grid_y] != "water" and self.array_tiles[grid_x-1,grid_y-1] != "water" and self.array_tiles[grid_x-4,grid_y-4] != "water":
                    tile1 = "tree"
                elif 20<r<25 and self.array_tiles[grid_x,grid_y] != "water" and self.array_tiles[grid_x-1,grid_y-1] != "water" and self.array_tiles[grid_x-4,grid_y-4] != "water":
                    tile1= "bush"
                elif 30<r<33 and self.array_tiles[grid_x,grid_y] != "water" and self.array_tiles[grid_x-1,grid_y-1] != "water" and self.array_tiles[grid_x-4,grid_y-4] != "water":
                    tile1="gold"
                elif 32<r<34 and self.array_tiles[grid_x,grid_y] != "water" and self.array_tiles[grid_x-1,grid_y-1] != "water" and self.array_tiles[grid_x-4,grid_y-4] != "water":
                    tile1="rock"
                else:
                    tile1 = ""

        else: tile1=""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx,miny],
            "tile": tile1,
            "collision": False if tile1 == "" and self.array_tiles[grid_x,grid_y] != "water" else True,
            "entity" : False
        }
        return out

    def cart_to_iso(self,x,y): #Coordonées rectangulaires en isométriques
        iso_x = x-y 
        iso_y = (x + y)/2
        return iso_x, iso_y

    def load_images(self):
        Towncenter = pygame.image.load("assets/Towncenter.png").convert_alpha()
        grass = pygame.image.load("assets/t_grass.png").convert_alpha()
        water = pygame.image.load("assets/t_water.png").convert_alpha()
        tree = pygame.image.load("assets/tree.png").convert_alpha()
        bush =pygame.image.load("assets/bush.png").convert_alpha()
        gold = pygame.image.load("assets/Gold.png").convert_alpha()
        rock = pygame.image.load("assets/Rock.png").convert_alpha()
        house = pygame.image.load("Buildings/House1.png").convert_alpha()
        return {"Towncenter": Towncenter, "grass": grass, "water": water, "tree": tree,"bush":bush,"gold":gold,"rock":rock,"House":house}

    def mouse_to_grid(self, x, y, scroll):
        # transformer le world position sans camera et offset
        world_x = x - scroll.x - self.map_tiles.get_width() / 2
        world_y = y - scroll.y
        # transformer to cart (inverse des pixels iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)
        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False
