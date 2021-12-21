import pygame

class Camera:

    def __init__(self, width, height):
        
        self.width = width
        self.height = height

        self.scroll = pygame.Vector2(0,0)
        self.dx = 0     #Difference in x value
        self.dy = 0     #Difference in y value
        self.speed = 15     #pixels

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        #x mouvement
        if mouse_pos[0] > self.width *0.97 and mouse_pos[0] < self.width-1: #If the x value in the mouse pos is almost at the edge of the screen
            self.dx = -self.speed  
        elif mouse_pos[0] < self.width * 0.03 and mouse_pos[0] > 0:
            self.dx = self.speed
        else:
            self.dx = 0

        #Y MOUVEMENT
        if mouse_pos[1] > self.height *0.97 and mouse_pos[1] < self.height-1:
            self.dy = -self.speed  
        elif mouse_pos[1] < self.height * 0.03 and mouse_pos[1] > 0:
            self.dy = self.speed
        else:
            self.dy = 0  

        #update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy
            
