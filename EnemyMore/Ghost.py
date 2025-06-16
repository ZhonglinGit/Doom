import Enemy
import pygame
import math
import angles
import Constant

class Ghost(Enemy.Enemy):
    def __init__(self, screen, player,map, x, y, name):
        '''x, y is the map x,y, need to * space'''
        super().__init__(screen, player,map, name)
        self.image = pygame.image.load("Doom\picture\ghost\ghost.png").convert_alpha()
        self.fullhealth = 5
        self.health = self.fullhealth
        self.width = 20
        self.midX = x * Constant.SPACE
        self.midY = y * Constant.SPACE

        self.skillTime = 0
        self.detlaTime = 1000
        self.skillFlag = False

    def update(self):
        
        self.angle = self.player.angle + 90
        halfWidth = self.width / 2
        rad = math.radians(self.angle)
        dx = halfWidth * math.cos(rad)
        dy = halfWidth * math.sin(rad)
        self.x = self.midX - dx
        self.y = self.midY - dy
        self.endx = self.midX + dx
        self.endy = self.midY + dy
        self.anglePtoStart = angles.normalize(math.degrees(math.atan2(self.y - self.player.y, self.x - self.player.x)))
        self.anglePtoEnd = angles.normalize(math.degrees(math.atan2(self.endy - self.player.y, self.endx - self.player.x)))

        angle = math.atan2(self.player.y - self.y, self.player.x - self.x)
        if pygame.time.get_ticks() - self.skillTime >= self.detlaTime:
              self.skillFlag = not self.skillFlag
        if self.skillFlag:
              angle = angle + 90
        self.midX += self.speed * math.cos(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midX -= self.speed * math.cos(angle)

        self.midY += self.speed * math.sin(angle)
        if not self.map.canYouMove(self.midX, self.midY):
                self.midY -= self.speed * math.sin(angle)

        if self.getDisToPlayer() < 10:
            self.player.getHit()
        
   

