import Enemy
import pygame
import math
import angles
import random
import Constant

#base on ghost, can stand there chang picture, then teleport to your back

class PhaseReaper(Enemy.Enemy):
    def __init__(self, screen, player,map, x, y, name):
        '''x, y is the map x,y, need to * space'''
        super().__init__(screen, player,map, name)
        self.image = pygame.image.load("Doom\picture\phase.PNG").convert_alpha()
        self.fullhealth = 4
        self.health = self.fullhealth
        self.speed = 4
        self.width = 20
        self.midX = x * Constant.SPACE
        self.midY = y * Constant.SPACE

        self.skillTime = 0
        self.detlaTime = 700
        self.skillFlag = False
        self.skilldir = 1

        #phase is the Invincible teleport animation
        self.phaseCool = 10000
        self.phaseDuration = 5000
        #for how long is next phase
        self.phaseTime = 0
        #for how long this will last
        self.phaseStartTime = 0

        #timer after phase you start can't see
        self.invisibilityDura = 1000
        self.isPhasing = False
        self.visible = True


    def update(self):
        now = pygame.time.get_ticks()

        if self.isPhasing:
            if now - self.phaseStartTime >= self.phaseDuration:
                #exit phase
                self.endPhase()
            elif now - self.phaseStartTime >= self.invisibilityDura:
                 self.visible = False
                 self.canGetHit = False
            else:
                 #during phase, don't do any thing
                 return
        elif now - self.phaseTime >= self.phaseCool:
             self.startPhase()
        
        else:
            # normal run time
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
    def render(self, depthList):
        if self.visible:
            super().render(depthList)
    

    def startPhase(self):
        # print("start")
        self.isPhasing = True
        #for how long this will last
        self.phaseStartTime = pygame.time.get_ticks()
        self.image = pygame.image.load("Doom\picture\phaseing.PNG").convert_alpha()
        #for how long is next phase
        self.phaseTime = pygame.time.get_ticks()
    
    def endPhase(self):
        '''apear at the back of the player'''
        # print("end")
        angler = math.radians(self.player.angle)
        disToFly = 100

        x = self.player.x - disToFly * math.cos(angler)
        y = self.player.y - disToFly * math.sin(angler)

        if self.map.canYouMove(x,y):
            self.midX = x
            self.midY = y
        else:
             self.midX, self.midY = self.randomGoodPos()

        self.image = pygame.image.load("Doom\picture\phase.PNG").convert_alpha()
        self.canGetHit = True
        self.isPhasing = False
        self.visible = True
             
    def randomGoodPos(self):
        run = True
        while run:
            disToFly = 100

            angler = random.uniform(-math.pi, math.pi)

            x = self.player.x + disToFly * math.cos(angler)
            y = self.player.y + disToFly * math.sin(angler)

            if self.map.canYouMove(x,y):
                 run = False
        return x,y
    




    