import pygame


WIDTH, HEIGHT = 1280, 720 #La définition de l'écran facilement modifiable
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
TILE_SIZE = 32
MAP_SIZE = 100
LES_RESSOURCES = {"WOOD", "FOOD", "GOLD", "STONE"}
NB_ARBRES = 20
FPS =60
def lerp(a,b,t):
    return a*(1-t) + b*t



def draw_text(screen, text, size, colour, pos):

    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)
