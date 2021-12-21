import pygame
#this still not working as it needs more details to be added
#these all are mob sublasses (mob is a meta classs that shall contain all living beings )
allMobs = pygame.sprite.Group()
allHumans = pygame.sprite.Group()
animals = pygame.sprite.Group()
passiveAnimals = pygame.sprite.Group()
hostileAnimals = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    """Base class for all mobs """
    def __init__(self, baseMoveSpeed, img, coords, size, health =None):
        #When you subclass Sprite, you must call this pygame.sprite.Sprite.__init__(self) before you add the sprite to any groups, or you will get an error.
        self.isDead = False
        self.causeOfDeath = None
        self.add(allmobs)#adds it to all my mobs

        self.animFrame =0
        self.timeLastFrameChange = 0
        self.animFrameDuration = 0.15
        if type(img) == list :
            self.animation = img
            self.lastAnimation = self.animation
            self.handleImage()
        else:
            self.image = img
            self.animation = None

        self.direction = 'right'
        #self.rect = pygame.Rect(map.cellsToPixels(coords), size) #this shuldshuld link it to the map
        self.truePos = (self.rect.topleft) #gives us the position of the top left side of the rectangle

        self.destination = None
        self.baseMoveSpeed = baseMoveSpeed
        self.moveSpeed = self.baseMoveSpeed

        self.health = health
        self.startHealth = health
        self.lastHealth = self.health
        self.drawHealthBar = False

        self.coords = coords

	def baseUpdate(self, dt):
        if not self.isDead:
            #self.coords = map.pixelsToCell(self.rect.center) this should determin the coordinates of a caracter
            self.updateMove(dt)    ### update move is gon be based on axel's code
            self.handleImage()
            self.blit()   #### the concept of blit aka bit block transfer is still a bit ambiguous to me so m still working on it
            if self.health is not None: self.handleHealth()

    #def handle image is related to the sprites it needs a bit of time


class HostileAnimal(Mob):
	"""Base class for animals that hunt and kill nearby humans"""
	def __init__(self, baseMoveSpeed, img, coords, size, chaseDistance, health, damage):
		"""chaseDistance is arbitrary i culd modify afterwards"""
		Mob.__init__(self, baseMoveSpeed, img, coords, size, health)
		self.add(animals)     # animals is a sprite group that makes it easier to manage collisions
		self.add(hostileAnimals)        #same goes for hostile animals
		self.chaseDistance, self.damage = chaseDistance, damage

	def animalUpdate(self):
		if not self.hunting :
			self.findPrey()
		if self.hunting:
			self.destination = self.hunting.coords
			if  self.rect.colliderect(self.hunting.rect): # in other words if he touches the human
				self.hunting.health -= self.damage
				if self.hunting.health < 1:
					self.hunting.causeOfDeath = 'been eaten by a %s' %(self.name)
					self.hunting = None
		self.baseUpdate(dt) # as i am basing my code on other codes i find online in addition to videos i find it that this base update function is necessary but m still delving into what it does actuaclly but m letting it here till i unveil it secrets
	# i feel as if i shuld sth in relation to wheter the animal is in the screen that's unveiled or not

	def findPrey(self):
		target = map.findNearestobject(self.coords, my.allHumans) #find nearestobject is a function that has yet to be defined but will be when the map is partially done
		if target and map.distanceTo(self.coords, target.coords) < self.chaseDistance: #so is distance to
			self.hunting = target

class lion(HostileAnimal):
	"""Lion ROAR"""
	runAnim = loadAnimationFiles('Lion/run')     # this is the adress in which lies the images of a runing lion
	def __init__(self, coords='randomGrass'):
		self.name = ' Lion'
		self.idleAnim = Lion.runAnim
		self.moveAnim = Lion.runAnim
		self.chaseSound = 'Lion roar'    #has yet to be downloaded
		self.attackSounds = ['Roar']
		HostileAnimal.__init__(self, 80, self.idleAnim, coords, (25, 15), 100, 200, 2600)


	def update(self, dt):
		self.animalUpdate(dt)


class PassiveAnimal(Mob):
	"""Base class for animals that do not interact with humans"""
	def __init__(self, baseMoveSpeed, img, coords, size):
		# here was a thing that i shuld remember implementing if stuff dont go too well
		Mob.__init__(self, baseMoveSpeed, img, coords, size)
		self.add(animals)
		self.add(passiveAnimals)

	def animalUpdate(self, dt):
		# this shud be modified so as to include some procedure that test wheter we can see the animal or not
		# i shuld make it move around itself a bit
		self.baseUpdate(dt)

################### i ll need time to work a bit on the other stuff for it might need special attention due to the sprites and stuff
