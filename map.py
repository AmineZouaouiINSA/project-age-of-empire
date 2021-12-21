##MODULES##

import pygame
import numpy

##VARIABLES A IMPORTER

from definitions import MAP_SIZE

##FONCTIONS##

#randomMap() : 

    #cree une map aleatoire au début de chaque partie : le biome de chaque tile est renvoyé dans un array de dimension 2.
    #generation aleatoire 
'''

Tout ce qui est entre cotes est obsolète mais servira peut-être un jour : ça patientera ici au cas où.

#mapGeneration : affiche la map à partir d'un array généré de façon aléatoire

def mapGeneration(size,window,array) :
    tileList = []
    for i in range(size) :
        tileList.append([])
    milieu = int(size*65/2)

    for x in range(0,size) :
        for y in range(0,size):
            window.blit(pygame.image.load("Textures/Tiles/t_"+array[y,x]+".png"),(milieu-33*x-16+33*y,x*16+y*16))
            tileList[x].append(tile(x,y,array[y,x]))

#noise : fonction pour bruiter une valeur. Avantages : à partir d'une valeur d'entrée, on a toujours la même valeur de sortie -> permet de reproduire un bruit malgré avec l'actualisation de la map si on possède une seed.
'''
def noise(seed,x,y) :
    x = (x >> seed//2) ^ x
    y = (y >> seed//2) ^ y
    noisedX = (x * (x * x * 60493 + 19990303) + 1376312589) & 0x7fffffff
    noisedY = (y * (y * y * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return 1.0 - (noisedX / 1073741824.0)

def randomMap() :
    from scipy.ndimage.interpolation import zoom
    #generation aleatoire : distribution uniforme de taille 4x4
    arr = numpy.random.uniform(size=(4,4))
    #zoome sur l'array d'un facteur 6
    arr = zoom(arr, MAP_SIZE/4)
    arr = arr > 0.8
    #if true : - . if false : #
    arr = numpy.where(arr, 'water', 'grass')
    return arr
