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
        self.fullhealth = 1
        self.health = self.fullhealth
        self.speed = 2.5
        self.width = 15
        self.midX = x * Constant.SPACE
        self.midY = y * Constant.SPACE

    def update(self):
        super().update()

        angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
        self.midX += self.speed * math.cos(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midX -= self.speed * math.cos(angle)

        self.midY += self.speed * math.sin(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midY -= self.speed * math.sin(angle)

       

   


        
    