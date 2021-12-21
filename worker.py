from pathlib import Path
import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from definitions import *
import time
class Personnage:
    def __init__(self, tile, world, camera, team):
        self.team = team
        self.world = world
        self.world.entities.append(self)
        self.camera = camera
        self.world.world[tile["grid"][0]][tile["grid"][1]]["entity"]=True
        self.tile = tile
        self.adj_tiles = self.adjacent_tiles(self.tile)

        self.image = pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk001.png')).convert_alpha()
        self.temp = 0
        self.en_attack = False
        self.moveright_animation = False
        self.moveleft_animation = False
        self.movestraight_animation = False
        self.moveback_animation = False
        self.dead = False
        self.sprites = []
        self.current_sprite = 0
        self.d = 0
        self.avancement = 0
        self.world.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.pos_x = tile["render_pos"][0]
        self.pos_y = tile["render_pos"][1]
        self.selected = False
        self.selected_enemies = []
        self.selection_box = pygame.Rect(self.pos_x + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 4,
                                         self.pos_y - self.image.get_height() + self.camera.scroll.y + 34, 24, 34)
        iso_poly = self.tile["iso_poly"] #coord isometrique
        self.iso_poly = None
        self.mouse_to_grid(0, 0, self.camera.scroll)
        self.create_path(tile["grid"][0], tile["grid"][1])
        self.path_index = 0
        self.grids = []


    def adjacent_tiles(self,t):
        return [self.world.world[t["grid"][0]+1][t["grid"][1]]   if (t["grid"][0]+1) < MAP_SIZE                                          else None,   #tile bas gauche
                self.world.world[t["grid"][0]][t["grid"][1]+1]   if (t["grid"][1]+1) < MAP_SIZE                                          else None,   #tile bas droite
                self.world.world[t["grid"][0]-1][t["grid"][1]]   if (t["grid"][0]-1) >= 0                                                else None,   #tile haut gauche
                self.world.world[t["grid"][0]][t["grid"][1]-1]   if (t["grid"][1]-1) >= 0                                                else None,   #tile haut droite
                self.world.world[t["grid"][0]-1][t["grid"][1]-1] if (t["grid"][0]-1) >= 0       and (t["grid"][1]-1) >= 0        else None, #tile haut
                self.world.world[t["grid"][0]+1][t["grid"][1]+1] if (t["grid"][0]+1) > MAP_SIZE and (t["grid"][1]-1) > MAP_SIZE  else None, #tile bas
                self.world.world[t["grid"][0]-1][t["grid"][1]+1] if (t["grid"][0]+1) >= 0       and (t["grid"][1]-1) > MAP_SIZE  else None, #tile droite
                self.world.world[t["grid"][0]+1][t["grid"][1]-1] if (t["grid"][0]+1) > MAP_SIZE and (t["grid"][1]-1) >=0         else None] #tile gauche



    def update_animation(self,speed):
        if self.moveright_animation == True:
            self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.moveright_animation = False

        elif self.moveleft_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.moveleft_animation = False


        elif self.movestraight_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.movestraight_animation = False

        elif self.en_attack == True:
            self.current_sprite += speed
            print(self.current_sprite)
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.en_attack = False
        elif self.dead == True:
            self.current_sprite += speed
            print(self.current_sprite)
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.dead = False

        self.image = self.sprites[int(self.current_sprite)]

    def direction(self,grid_start,grid_dest):
        dx = grid_start[0] - grid_dest[0]
        dy = grid_start[1] - grid_dest[1]
        direction = 0

        if (2 > dx > 1 and dy < 0 ):
            print("Direction en haut")
            direction = 15

        if( 25 > dx > 10 and 25 > dy > 10):
            print("Direction en bas à droite , dx = ",dx," et dy = ",dy)
            direction = 5
        elif (dx > 0 and  (-30 < dy < -6)):
            print("Direction en haut à droite , dx = ",dx," et dy = ",dy)
            direction = 1

        elif (dx < 0 and dy > 0):
            print("Direction en bas à gauche")
            direction = 7

        elif (dx < 0 and dy < 0):
            print("Direction en haut à gauche")
            direction = 10

        elif(dx > 0 and dy <= 1):
            print("Direction à droite")
            direction = 3
        elif(dx < 0 and dy <= 1):
            print("Direction à gauche")
            direction = 9
        elif (dy > 0 and dx <= 1):
            print("Direction bas")
            direction = 6
        elif (dy < 0 and dx <= 1):
            print("Direction Haut")
            direction = 12

        return direction

    def delete(self,unit) :
        self.world.entities.remove(unit)
        self.world.workers[unit.tile["grid"][0]][unit.tile["grid"][1]] = None
        self.world.world[unit.tile["grid"][0]][unit.tile["grid"][1]]["entity"] = False
        unit.world = None

    def close_tile(self,t) :

        for adj_tile in self.adjacent_tiles(t) :
            if adj_tile != None :
                if not adj_tile["collision"] :
                    return adj_tile;
        return None;

    def create_path(self, x, y):
        searching_for_path = True
        while searching_for_path:
            self.dest_tile = self.world.world[x][y]
            if not self.dest_tile["collision"] :
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
            elif self.dest_tile["entity"] :
                if self.close_tile(self.dest_tile) != None :
                    self.dest_tile = self.close_tile(self.dest_tile)
                    self.create_path(self.dest_tile["grid"][0],self.dest_tile["grid"][1])
                break
            else:
                break

    def change_tile(self, new_tile):
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"]=False
        self.world.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.workers[new_tile[0]][new_tile[1]] = self
        self.tile = self.world.world[new_tile[0]][new_tile[1]]
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["entity"]=True
        self.adj_tiles=self.adjacent_tiles(self.tile)

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.world.map_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def update(self):
        #self.animation_walk_straight()
        # Updating mouse position and action and the grid_pos
        mx,my = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()
        grid_pos = self.mouse_to_grid(mx, my, self.camera.scroll)

        self.selection_box.update(self.pos_x + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 47,
                                  self.pos_y - self.image.get_height() + self.camera.scroll.y + 50, 28, 60)

        # Selection polygon
        pos_poly = [self.pos_x + self.world.map_tiles.get_width() / 2 + self.camera.scroll.x + 47,
                    self.pos_y - self.image.get_height() + self.camera.scroll.y + 50]
        self.iso_poly = [(pos_poly[0] - 10, pos_poly[1] + 44), (pos_poly[0] + 15, pos_poly[1] + 29),
                         (pos_poly[0] + 40, pos_poly[1] + 44), (pos_poly[0] + 15, pos_poly[1] + 59)]

        # collision matrix (for pathfinding and buildings)
        self.world.collision_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 0
        self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["collision"] = True

        # update des animations

        #self.animation_walk_straight()

        if self.selection_box.collidepoint(mx,my):
            if mouse_action[0]:      
                if self.selected == False :
                    self.selected = True
                    self.world.selected_units.append(self)

        if self.selected:
            if mouse_action[2]:
                self.animation_walk_straight()
                #print(grid_pos[0], grid_pos[1])
                #if len(self.grids) != 0 :
                #    self.d = self.direction(grid_pos, self.grids[len(self.grids) - 1])
                #    print(self.d)
                #else:
                   # self.grids.append(grid_pos)
                if self.team != "enemy" :
                    self.selected_enemies = [unit for unit in self.world.selected_units if unit.team == "enemy"]
                    self.selected = False
                    self.world.selected_units.remove(self)
                    if self.selected_enemies != [] :
                        self.create_path(self.selected_enemies[0].tile["grid"][0], self.selected_enemies[0].tile["grid"][1])
                        #go bagarre
                        #self.animation_attack_straight()
                    else :
                        '''if len(self.grids) != 0 :
                                self.d = self.direction(grid_pos, self.grids[len(self.grids) - 1])
                                print(self.d)
                            else:
                                self.grids.append(grid_pos)
                            if self.d == 1:
                                self.animation_walk_straight()
                            elif self.d == 12:
                                self.animation_walk_back()
                            elif self.d == 3:
                                self.animation_walk_straight()
                            elif self.d == 5:
                                self.animation_walk_top_left()
                            elif self.d == 6:
                                self.animation_walk_straight()
                            elif self.d == 7:
                                self.animation_walk_straight()
                            elif self.d == 9:
                                self.animation_walk_top_left()
                            elif self.d == 10:
                                self.animation_walk_top_left()'''
                        self.create_path(grid_pos[0], grid_pos[1])
                            
                else :
                    selected_players= [unit for unit in self.world.selected_units if unit.team == "player"]
                    '''if self.d == 1:
                        self.animation_walk_straight()
                    elif self.d == 12:
                        self.animation_walk_back()
                    elif self.d == 3:
                        self.animation_walk_straight()
                    elif self.d == 5:
                        self.animation_walk_top_left()
                    elif self.d == 6:
                        self.animation_walk_straight()
                    elif self.d == 7:
                        self.animation_walk_straight()
                    elif self.d == 9:
                        self.animation_walk_top_left()
                    elif self.d == 10:
                        self.animation_walk_top_left()
                        #self.update_animation(0.2)
                    elif self.d == 15:
                        self.animation_walk_back()'''
                    if selected_players == [] :
                        self.selected = False
                        self.world.selected_units.remove(self)

        if self.selected_enemies != [] and not self.world.world[self.selected_enemies[0].tile["grid"][0]][self.selected_enemies[0].tile["grid"][1]]["entity"] :
            self.selected_enemies.pop(0)
            if self.selected_enemies != []:
                self.create_path(self.selected_enemies[0].tile["grid"][0], self.selected_enemies[0].tile["grid"][1])
            else :
                self.create_path(self.tile["grid"][0], self.tile["grid"][1])

        if self.selected_enemies != [] and self.tile in self.selected_enemies[0].adj_tiles and self.world.world[self.selected_enemies[0].tile["grid"][0]][self.selected_enemies[0].tile["grid"][1]]["entity"]:
            self.animation_attack_straight()
            while self.selected_enemies[0].health > 0 :
                self.selected_enemies[0].health = self.selected_enemies[0].health - self.attack
                self.selected_enemies[0].animation_death()

            print("dead")
            self.delete(self.selected_enemies[0])
            self.selected_enemies.pop(0)
            if self.selected_enemies != []:
                self.create_path(self.selected_enemies[0].tile["grid"][0], self.selected_enemies[0].tile["grid"][1])
            else :
                self.create_path(self.tile["grid"][0], self.tile["grid"][1])

        if self.path_index <= len(self.path) - 1:
            self.movestraight_animation = True
            new_pos = self.path[self.path_index]
            new_real_pos = self.world.world[new_pos[0]][new_pos[1]]["render_pos"]
            if self.avancement < 1:
                self.avancement+= (1 / 135) * 5
                self.avancement = round(self.avancement, 3)
            else:
                self.avancement = 1
            self.pos_x = round(lerp(self.tile["render_pos"][0], new_real_pos[0], self.avancement), 3)
            self.pos_y = round(lerp(self.tile["render_pos"][1], new_real_pos[1], self.avancement), 3)

            if self.pos_x == new_real_pos[0] and self.pos_y == new_real_pos[1]:
                # update position in the world
                self.world.collision_matrix[self.tile["grid"][1]][self.tile["grid"][0]] = 1  # Free the last tile from collision
                self.world.world[self.tile["grid"][0]][self.tile["grid"][1]]["collision"] = False

            if self.pos_x == new_real_pos[0] and self.pos_y == new_real_pos[1]:  # update position in the world
                self.change_tile(new_pos)
                self.path_index += 1
                self.avancement = 0
        else:
            self.movestraight_animation = False
        #self.update_animation(0.2)

class Archer(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__( tile, world, camera, team)
        self.type_perso = "Archer"
        self.health = 35
        self.attack = 3
        self.costfood = 50
        self.training_time_in_sec = 30
        self.rateoffire = 1.4
        self.range = 5
        self.speed = 1.2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40

        # ANIMATION IMAGE WALK
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk001.png')))
        self.image = self.sprites[self.current_sprite]


    def animation_walk_back(self):
        self.moveright_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk040.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk041.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk042.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk043.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk044.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk045.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk046.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk047.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk048.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk049.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk050.png')))

    def animation_walk_left(self):
        self.moveleft_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk021.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk022.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk023.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk024.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk025.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk026.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk027.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk028.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk029.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk030.png')))



    def animation_walk_top_left(self):
        self.moveleft_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk031.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk032.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk033.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk034.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk035.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk036.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk037.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk038.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk039.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk040.png')))


    def animation_walk_bottom_left(self):
        self.moveleft_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk011.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk012.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk013.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk014.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk015.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk016.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk017.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk018.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk019.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk020.png')))

    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk010.png')))

        ########################"

    def animation_attack_straight(self):
        self.en_attack = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Attack/Archerattack010.png')))

    def animation_death(self):
        self.dead = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Die/Archerdie010.png')))



class Clubman(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Clubman"
        self.health = 40
        self.attack = 3
        self.costfood = 50
        self.training_time_in_sec = 26
        self.rateoffire = 1.5
        self.speed = 1.2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40
        # ANIMATION IMAGE WALKING
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk001.png')))
        self.image = self.sprites[self.current_sprite]

    def animation_death(self):
        self.dead = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie010.png')))



    def animation_walk_back(self):
        self.moveback_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk061.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk062.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk063.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk064.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk065.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk066.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk067.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk068.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk069.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk070.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk071.png')))


    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []

        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk010.png')))



    def animation_attack_straight(self):
        # self.attack(target)
        self.en_attack = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack010.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack011.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack012.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack013.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack014.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack015.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack016.png')))

    def animation_walk_top_left(self):
        self.moveleft_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk031.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk032.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk033.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk034.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk035.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk036.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk037.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk038.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk039.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk040.png')))


class Axemen(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Axemen"
        self.health = 50
        self.attack = 5
        self.costfood = 50
        self.training_time_in_sec = 28
        self.rateoffire = 1.5
        self.speed = 1.2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40

        # ANIMATION IMAGE WALKING

        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack001.png')))
        self.image = self.sprites[self.current_sprite]

    def animation_death(self):
        self.dead = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Die/Axethrowerdie010.png')))




    def animation_walk_back(self):
        self.moveback_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk061.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk062.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk063.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk064.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk065.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk066.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk067.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk068.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk069.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk070.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk071.png')))


    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Walk/Axethrowerwalk010.png')))






    def animation_attack_straight(self):
        # self.attack(target)
        self.en_attack = True
        self.sprites = []

        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack010.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack011.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack012.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack013.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack014.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack015.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Axe Thrower/Attack/Axethrowerattack016.png')))



        ########################"







class Scout(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Scout"
        self.health = 60
        self.attack = 3
        self.costfood = 90
        self.training_time_in_sec = 30
        self.rateoffire = 1.5
        self.speed = 2
        self.upgradecost = 100
        self.upgrade_time_in_sec = 40
        # ANIMATION IMAGE WALKING

        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk001.png')))
        self.image = self.sprites[self.current_sprite]

    def animation_death(self):
        self.dead = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Die/Scoutdie010.png')))






    def animation_walk_back(self):
        self.moveback_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk041.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk042.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk043.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk044.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk045.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk046.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk047.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk048.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk049.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk050.png')))



    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Walk/Scoutwalk010.png')))


        #self.image = self.sprites[self.current_sprite]


        ########################"

    def animation_attack_straight(self):
        # self.attack(target)
        self.en_attack = True
        self.sprites = []

        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout/Attack/Scoutattack010.png')))





        ###############################"""

class Villageois(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__(tile, world, camera, team)
        self.type_perso = "Villageois"
        self.health = 25
        self.attack = 3
        self.costfood = 50
        self.training_time_in_sec = 20
        self.rateoffire = 1.5
        self.speed = 1.1
        # ANIMATION IMAGE WALKING

        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk001.png')))
        self.image = self.sprites[self.current_sprite]


    def animation_death(self):
        self.dead = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie010.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie011.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Die/Villagerdie012.png')))




    def animation_walk_back(self):
        self.moveback_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk061.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk062.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk063.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk064.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk065.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk066.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk067.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk068.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk069.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk070.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk071.png')))




    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []


        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk010.png')))
        #self.current_sprite = 0

        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Build & Repair/Walk/Villagerwalk010.png')))


        #self.image = self.sprites[self.current_sprite]


        ########################"

    def animation_attack_straight(self):
        # self.attack(target)
        self.en_attack = True
        self.sprites = []

        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract001.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract005.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract006.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract007.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract008.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract009.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract010.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract011.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract012.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract013.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract014.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Villager/Male/Farm/Attack/Villageract015.png')))







        ###############################"""


class ScoutShip(Personnage):
    def __init__(self, tile, world, camera, team):
        super().__init__(tile, world, camera, team)
        self.type_perso = "ScoutShip"
        self.health = 120
        self.attack = 5
        self.costfood = 135
        self.training_time_in_sec = 45
        self.rateoffire = 1.5
        self.speed = 1.75
        self.upgradecost = 225
        self.upgrade_time_in_sec = 40

        # ANIMATION IMAGE WALKING

        self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship001.png')))
        self.image = self.sprites[self.current_sprite]
    def animation_death(self):
        self.dead = True
        pass
    def animation_walk_straight(self):
        self.movestraight_animation = True
        self.sprites = []

        self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship002.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship003.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship004.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship005.png')))

    def animation_attack_straight(self):
        pass

        ########################"
