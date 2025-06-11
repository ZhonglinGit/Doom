import Enemy
import pygame
import math
import angles

class Devil(Enemy.Enemy):
    def __init__(self, screen, player,map, x, y, name):
        '''x, y is the map x,y, need to * space'''
        super().__init__(screen, player,map, name)
        self.image = pygame.image.load("Doom\picture\devil.PNG").convert_alpha()
        self.fullhealth = 5
        self.width = 20
        self.midX = x
        self.midY = y
        print(f"[Debug] Devil enemy x type: {type(self.midX)}, value: {self.midX}")

   


        
    