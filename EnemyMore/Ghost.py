import Enemy
import pygame
import math
import angles
import random
import Constant

class Ghost(Enemy.Enemy):
    def __init__(self, screen, player,map, x, y, name):
        '''x, y is the map x,y, need to * space'''
        super().__init__(screen, player,map, name)
        self.image = pygame.image.load("Doom\picture\ghost\ghost.png").convert_alpha()
        self.fullhealth = 1
        self.health = self.fullhealth
        self.speed = 3
        self.width = 20
        self.midX = x * Constant.SPACE
        self.midY = y * Constant.SPACE

        self.skillTime = 0
        self.detlaTime = 1000
        self.skillFlag = False
        self.skilldir = 1

    def update(self):
        super().update()
  
        angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
        if pygame.time.get_ticks() - self.skillTime >= self.detlaTime:
              self.skillFlag = not self.skillFlag
              self.skillTime = pygame.time.get_ticks()
              self.skilldir = random.choice([-1,1]) 
        if self.skillFlag:
              angle = angle + math.pi /2 * self.skilldir
        self.midX += self.speed * math.cos(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midX -= self.speed * math.cos(angle)

        self.midY += self.speed * math.sin(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midY -= self.speed * math.sin(angle)

   

