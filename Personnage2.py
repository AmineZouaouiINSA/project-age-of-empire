from pathlib import Path
import pygame, random
import math
from Mouvement import *
from camera import Camera
from abc import abstractproperty, abstractmethod, ABCMeta

class Personnage(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.posDepart = [self.pos_x, self.pos_y]
        self.posArrivee = [pos_x, pos_y]
        self.progression = 0
        self.en_attack = False
        self.moveright_animation = False
        self.moveleft_animation = False
        self.movestraight_animation = False
        self.sprites = []
        self.current_sprite = 0

        self.selected = False

        @property
        def type_perso(self):
            pass

        @property
        def attack(self):
            pass

        @property
        def maxHealth(self):
            pass

        @property
        def health(self):
            pass

        @property
        def costfood(self):
            pass

        @property
        def training_time_in_sec(self):
            pass

        @property
        def rateoffire(self):
            pass

        @property
        def range(self):
            pass

        @property
        def speed(self):
            pass

    def direction(self,mx,my):
        dx = self.posArrivee[0] - self.pos_x
        dy = self.posArrivee[1] - self.pos_y
        direction = 0

        if( 250 > dx > 100 and 250 > dy > 100):
            print("Direction en bas à droite , dx = ",dx," et dy = ",dy)


        elif (dx > 0 and  (-300 < dy < -59)):
            print("Direction en haut à droite , dx = ",dx," et dy = ",dy)
            direction = 3

        elif (dx < 0 and dy > 0):
            print("Direction en bas à gauche")
            direction = 2

        elif (dx < 0 and dy < 0):
            print("Direction en haut à gauche")
            direction = 1

        elif(dx > 0 and dy <= 1):
            print("Direction à droite")
        elif(dx < 0 and dy <= 1):
            print("Direction à gauche")
        elif (dy > 0 and dx <= 1):
            print("Direction bas")
        elif (dy < 0 and dx <= 1):
            print("Direction Haut")

        return direction



    def gettype(self):
        return self.type_perso

    def gethealth(self):
        return self.health

    def deal_damage(self,damage):
        self.health -= damage

    def attack(self,target):
        pass

    def setpos(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def getpos(self):
        return self.pos_x,self.pos_y

    def movestraight(self):
        self.movestraight_animation = True

    def moveleft(self):
        self.moveleft_animation = True

    def moveright(self):
        self.moveright_animation = True

    def en_attack(self):
        self.enattack = True

    def update(self, window):
        self.pos_darrivee()
        self.update_movement()
        self.update_animation(0.2)
        self.draw(window)

    def selection(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            print("Collision")
            self.selected = True
        else:
            self.selected = False

    def pos_darrivee(self):
        if self.selected and pygame.mouse.get_pressed()[2]:
            [self.posArrivee[0], self.posArrivee[1]] = pygame.mouse.get_pos()
            self.posDepart[0], self.posDepart[1] = (self.pos_x, self.pos_y)
            self.progression = 0

    def update_movement(self):
        distance = math.sqrt((self.posArrivee[0] - self.posDepart[0]) * (self.posArrivee[0] - self.posDepart[0]) + (
                self.posArrivee[1] - self.posDepart[1]) * (self.posArrivee[1] - self.posDepart[1]))
        if distance != 0:
            dt = 1 / distance
            if self.progression < 1:
                self.progression += self.speed * dt
            else:
                self.progression = 1
            a = [self.pos_x, self.pos_y]
            self.pos_x = lerp(self.posDepart[0], self.posArrivee[0], self.progression)
            self.pos_y = lerp(self.posDepart[1], self.posArrivee[1], self.progression)
            self.rect.move_ip(round(self.pos_x) - round(a[0]), round(self.pos_y) - round(a[1]))

    def update_animation(self, speed):
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
            # print(self.current_sprite)
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.movestraight_animation = False

        elif self.en_attack == True:
            self.current_sprite += speed
            # print(self.current_sprite)
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.en_attack = False
        self.image = self.sprites[int(self.current_sprite)]

    def draw(self,window):
        window.blit(self.image, (self.pos_x ,self.pos_y))
        #pygame.draw.rect(window, (0,0,255), self.rect)


class Archer(Personnage):
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
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

        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk001.png')))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(midbottom=(self.pos_x, self.pos_y))
        self.rect.topleft = [self.pos_x, self.pos_y]


    def update(self, window):
        super().update(window)
        #

        self.animation_walk_straight()
        #self.animation_walk_bottom_right()
        #self.animation_walk_left()
        #self.animation_walk_top_left()
        #self.animation_walk_bottom_left()
        #self.animation_attack_straight()

    def animation_walk_bottom_right(self):
        self.moveright_animation = True
        self.sprites = []
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk060.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk061.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk062.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk063.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk064.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk065.png')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk066.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk067.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk068.jpg')))
        self.sprites.append(pygame.image.load(Path('Sprites/Archer/Walk/Archerwalk069.jpg')))

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
        # self.attack(target)
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

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

class Villageois(Personnage):
       def __init__(self, pos_x, pos_y):
            super().__init__(pos_x, pos_y)
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
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.pos_x, self.pos_y]

       def update(self, window):
            super().update(window)
            self.animation_walk_straight()
            #self.animation_attack_straight()

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
            self.current_sprite = 0

            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.topleft = [self.pos_x, self.pos_y]
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

            self.current_sprite = 0

            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.topleft = [self.pos_x, self.pos_y]
            ###############################"""

class Clubman(Personnage):
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
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
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, window):
        super().update(window)
        self.animation_walk_straight()
        #self.animation_attack_straight()

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
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

        ########################"

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



        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]


class Axemen(Personnage):
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
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
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, window):
        super().update(window)
        self.animation_walk_straight()
        #self.animation_attack_straight()

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
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]


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

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
        ########################"

class ScoutShip(Personnage):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
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
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, window):
        super().update(window)
        self.animation_walk_straight()

    def animation_walk_straight(self):
            self.movestraight_animation = True
            self.sprites = []

            self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship002.png')))
            self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship003.png')))
            self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship004.png')))
            self.sprites.append(pygame.image.load(Path('Sprites/Scout Ship (BETA unit)/Scout Ship005.png')))

            self.current_sprite = 0

            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.topleft = [self.pos_x, self.pos_y]
            ########################"

class Scout(Personnage):
    def __init__(self,pos_x,pos_y):
        super().__init__(pos_x,pos_y)
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
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update(self, window):
        super().update(window)
        self.animation_walk_straight()
        #self.animation_attack_straight()

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
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
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


        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]
        ###############################"""





