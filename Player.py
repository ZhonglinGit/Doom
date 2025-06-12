
import Constant
import pygame
import math

class Player():

    def __init__(self):
        self.x = 1 * Constant.SPACE
        self.y = 1 * Constant.SPACE
        self.angle = 0 #with respect to the big map
        self.angleL = 0
        self.angleR = 0

        self.viewDis = 160
        self.fieldOfView = 60  # degrees
        self.deltaAngle = self.fieldOfView / Constant.WIDTH  # degrees per ray

        self.speedInit = 3
        self.speed =  self.speedInit
        self.Aspeed = 2

        self.fireGap = 100  #ms
        self.fireOldTime = 0
        self.map = "xxx"

        self.energyBarMax = 2000
        self.energy = self.energyBarMax
        self.energyGain = 10
        self.speedCost = 10
        self.bulletCost = 400
        self.isSpeeding = False

        self.pointer = pygame.image.load("Doom\picture\point.PNG").convert_alpha()


    def inputMove(self, enemy):
        keys = pygame.key.get_pressed()
        dx = self.speed * math.cos(math.radians(self.angle)) # back and forth movement
        dy = self.speed * math.sin(math.radians(self.angle))
        
        # for move side way
        dRightX = self.speed * math.cos(math.radians(self.angle + 90))
        dRightY = self.speed * math.sin(math.radians(self.angle + 90))

        if keys[pygame.K_LSHIFT] and self.energy > 0:
            self.speed = self.speedInit * 2
            self.energy -= self.speedCost
            self.isSpeeding = True
            
        else:
            self.speed = self.speedInit
            self.isSpeeding = False

        print(self.isSpeeding)

        # back
        if keys[pygame.K_s]:
            self.x -= dx
            # if you run in to a wall, undo the move
            if not self.map.canYouMove(self.x,self.y ):
                self.x += dx
            
            self.y -= dy
            if not self.map.canYouMove(self.x,self.y ):
                self.y += dy


        # forward
        if keys[pygame.K_w]:

            self.x += dx
            if not self.map.canYouMove(self.x,self.y ):
                self.x -= dx

            self.y += dy
            if not self.map.canYouMove(self.x,self.y ):
                self.y -= dy


        if keys[pygame.K_d]:
            # y 
            self.y += dRightY
            if not self.map.canYouMove(self.x, self.y):
                self.y -= dRightY

            # x
            self.x += dRightX
            if not self.map.canYouMove(self.x, self.y):
                self.x -= dRightX

        if keys[pygame.K_a]:
            #y
            self.y -= dRightY
            if not self.map.canYouMove(self.x, self.y):
                self.y += dRightY

            #X
            self.x -= dRightX
            if not self.map.canYouMove(self.x, self.y):
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

        #shot
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            if pygame.time.get_ticks() - self.fireOldTime > self.fireGap and self.energy - self.bulletCost > 0:
                self.fireOldTime = pygame.time.get_ticks()
                self.energy -= self.bulletCost
                for e in enemy:
                    print(e.didGotShot())
                

        self.angle = self.angle

        self.angleL = self.angle - (self.fieldOfView //2)
        self.angleR = self.angle + (self.fieldOfView //2)

        if not self.isSpeeding:
            self.energy += self.energyGain

    
    def renderUI(self):
        pass
