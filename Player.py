
import Constant
import pygame
import math

class Player():

    def __init__(self, screen):
        self.x = 1 * Constant.SPACE
        self.y = 1 * Constant.SPACE
        self.angle = 0 #with respect to the big map
        self.angleL = 0
        self.angleR = 0

        self.viewDis = 240
        self.fieldOfView = 60  # degrees
        self.deltaAngle = self.fieldOfView / Constant.WIDTH  # degrees per ray

        self.speedInit = 4
        self.speed =  self.speedInit
        self.Aspeed = 2

        self.Fullhealth = 10
        self.health = self.Fullhealth
        self.invincibilityTime = 500
        self.healthTime = 0

        self.fireGap = 500  #ms
        self.damage = 1
        self.fireOldTime = 0
        self.map = "xxx"

        self.energyBarMax = 2000
        self.energy = self.energyBarMax
        self.energyGain = 10
        self.speedCost = 10
        self.bulletCost = 400
        self.isSpeeding = False

        self.twoGun = False
        self.blinkFrame = False

        self.screen = screen
        self.pointer = pygame.image.load("Doom\picture\point.PNG").convert_alpha()
        
        self.shotSound = ""
        self.mouseFlag = False
        self.lastM = False

    def getHit(self):
        if self.blinkFrame:
            #don'f grt hit when speed up
            if (pygame.time.get_ticks() - self.healthTime >= self.invincibilityTime) and not self.isSpeeding:
                self.healthTime = pygame.time.get_ticks()
                self.health -= 1

        else:
            if pygame.time.get_ticks() - self.healthTime >= self.invincibilityTime:
                self.healthTime = pygame.time.get_ticks()
                self.health -= 1
    
    def renderUI(self):
        if self.twoGun:
            pointerleft = pygame.image.load("Doom\picture\pointerleft.PNG").convert_alpha()
            pointerRight =  pygame.image.load("Doom\picture\pointerright.PNG").convert_alpha()

            pygame.draw.line(self.screen, (0,255,0), (Constant.WIDTH // 3, 0),(Constant.WIDTH // 3 , 300) )
            pygame.draw.line(self.screen, (0,255,0), (Constant.WIDTH // 3 * 2, 0),(Constant.WIDTH // 3 *  2, 300) )

            self.screen.blit(pointerleft,(Constant.WIDTH // 3 - pointerleft.get_width() +50, 80))
            self.screen.blit(pointerRight,(Constant.WIDTH // 3 * 2, 80))

        else:
            scaledPointer = pygame.transform.scale(self.pointer, (500,500))
            self.screen.blit(scaledPointer,(Constant.WIDTH // 2, 150))

        height = 20

        #health
        healthScale = 20
        healthx, healthy = 10, 10

        #base
        pygame.draw.rect(self.screen, (0, 0, 0), (healthx, healthy, self.Fullhealth * healthScale,height ))
        #health
        pygame.draw.rect(self.screen, (200, 50, 50), (healthx, healthy, self.health * healthScale,height ))

        #energy bar
        scale = 0.1
        #start point
        x,y = 10, 35
        

        #base
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.energyBarMax * scale,height ))
        #energy
        pygame.draw.rect(self.screen, (0, 200, 255), (x, y, self.energy * scale,height ))

        #bullet gride
        bulletNum = self.energyBarMax // self.bulletCost
        for i in range(bulletNum):

            pygame.draw.line(self.screen, 
                             (0, 0, 0), 
                             ((i + 1) * self.bulletCost * scale + x, y),
                             ((i + 1) * self.bulletCost * scale + x, y + height), 2 )

    def inputMove(self, enemy):
        self.health = max(0, self.health)
        keys = pygame.key.get_pressed()
        dx = self.speed * math.cos(math.radians(self.angle)) # back and forth movement
        dy = self.speed * math.sin(math.radians(self.angle))
        
        # for move side way
        dRightX = self.speed * math.cos(math.radians(self.angle + 90))
        dRightY = self.speed * math.sin(math.radians(self.angle + 90))

        #if you use all the energy you need to press again to speed up again
        flag = True

        #when energy is zero no speed up and can't speed up
        if self.energy == 0:
            self.isSpeeding = False
            flag = False
        #when not pressing, can speed up
        if not keys[pygame.K_LSHIFT]:
            flag = True
        #the speed up part
        if self.energy > 0 and keys[pygame.K_LSHIFT] and flag:
            self.speed = self.speedInit * 2
            self.energy -= self.speedCost
            if self.energy <0:
                self.energy = 0
            self.isSpeeding = True
        else:
            #normal speed when not speeding
            if not self.isSpeeding:
                self.speed = self.speedInit
        

        if keys[pygame.K_LSHIFT]:
            flag = True

        if not keys[pygame.K_LSHIFT] or self.energy <= 0:
            flag = False
            self.isSpeeding = False
        

        if flag and keys[pygame.K_LSHIFT]:
            self.speed = self.speedInit * 2
            self.energy -= self.speedCost
            if self.energy <0:
                self.energy = 0
            self.isSpeeding = True


        if not self.isSpeeding and self.energy < self.energyBarMax:
            self.energy += self.energyGain
            if self.energy > self.energyBarMax:
                self.energy = self.energyBarMax

        # print(self.isSpeeding)

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

        if keys[pygame.K_m] and not self.lastM:
            self.mouseFlag = not self.mouseFlag

            if self.mouseFlag :
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                
            else:
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(False)
               

        self.lastM = keys[pygame.K_m] 
        #shot
        if self.twoGun:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if pygame.time.get_ticks() - self.fireOldTime > self.fireGap and self.energy - self.bulletCost > 0:
                    self.fireOldTime = pygame.time.get_ticks()
                    self.energy -= self.bulletCost
                    for e in enemy:
                        e.didGotShotLeft(self.damage)
                        e.didGotShotRight(self.damage)
        else:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if pygame.time.get_ticks() - self.fireOldTime > self.fireGap and self.energy - self.bulletCost > 0:
                    self.fireOldTime = pygame.time.get_ticks()
                    self.energy -= self.bulletCost
                    self.shotSound.play()
                    for e in enemy:
                        e.didGotShot(self.damage)
                

        self.angle = self.angle

        self.angleL = self.angle - (self.fieldOfView //2)
        self.angleR = self.angle + (self.fieldOfView //2)

        

        

    

