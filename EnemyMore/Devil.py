import Enemy
import pygame
import math
import angles
import Constant

class Devil(Enemy.Enemy):
    def __init__(self, screen, player,map, x, y, name):
        '''x, y is the map x,y, need to * space'''
        super().__init__(screen, player,map, name)
        self.image = pygame.image.load("Doom\picture\devil\walk\devil_walk1.png").convert_alpha()
        self.fullhealth = 5
        self.health = self.fullhealth
        self.width = 20
        self.midX = x * Constant.SPACE
        self.midY = y * Constant.SPACE
   


        
    