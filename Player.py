
WIDTH, HEIGHT = 640, 480
import pygame
import math

class Player():

    def __init__(self, map):
        self.x = 4 * 30
        self.y = 4 * 30
        self.angle = 0 #with respect to the big map
        self.viewDis = 360
        self.fieldOfView = 60  # degrees
        self.deltaAngle = self.fieldOfView / WIDTH  # degrees per ray
        self.speed =  3
        self.Aspeed = 2
        self.angleL = 0
        self.angleR = 0
        self.map = map

    def canYouMove(self, x, y):
        mapX = int(x / self.map.space)
        mapY = int(y / self.map.space)
        
      
        if self.map.map[mapY][mapX] == 1:
            return False

        return True
    def inputMove(self):
        keys = pygame.key.get_pressed()
        dx = self.speed * math.cos(math.radians(self.angle)) # back and forth movement
        dy = self.speed * math.sin(math.radians(self.angle))

        # for move side way
        dRightX = self.speed * math.cos(math.radians(self.angle + 90))
        dRightY = self.speed * math.sin(math.radians(self.angle + 90))

        # back
        if keys[pygame.K_s]:
            self.x -= dx
            # if you run in to a wall, undo the move
            if not self.canYouMove(self.x,self.y ):
                self.x += dx
            
            self.y -= dy
            if not self.canYouMove(self.x,self.y ):
                self.y += dy


        # forward
        if keys[pygame.K_w]:

            self.x += dx
            if not self.canYouMove(self.x,self.y ):
                self.x -= dx

            self.y += dy
            if not self.canYouMove(self.x,self.y ):
                self.y -= dy


        if keys[pygame.K_d]:
            # y 
            self.y += dRightY
            if not self.canYouMove(self.x, self.y):
                self.y -= dRightY

            # x
            self.x += dRightX
            if not self.canYouMove(self.x, self.y):
                self.x -= dRightX

        if keys[pygame.K_a]:
            #y
            self.y -= dRightY
            if not self.canYouMove(self.x, self.y):
                self.y += dRightY

            #X
            self.x -= dRightX
            if not self.canYouMove(self.x, self.y):
                self.x += dRightX

        
        deltaPos =  pygame.mouse.get_rel()[0] 

        self.angle += deltaPos
        if keys[pygame.K_i]:
            self.angle -= self.Aspeed
        if keys[pygame.K_p]:
            self.angle += self.Aspeed

        if keys[pygame.K_m]:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

        self.angle = self.angle

        self.angleL = self.angle - (self.fieldOfView //2)
        self.angleR = self.angle + (self.fieldOfView //2)
