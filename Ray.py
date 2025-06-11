#zhonglin
#2025 05 23

import pygame
import math
import numpy
import sympy
import EnemyMore.Devil
import Player
import Enemy
import RayCasting
import EnemyMore
import Maploader
import Constant

pygame.init()
screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()


class Map():
    def __init__(self):
        
        self.map = [[]]
        self.space = 60
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.color = (255,0, 0)
    
    def getmap(self):
        return self.map
    def canYouMove(self, x, y):
        mapX = int(x / self.space)
        mapY = int(y / self.space)
        
      
        if self.map[mapY][mapX] == 1:
            return False

        return True

class Game:
    def __init__(self):
        #up date this at new level
        self.map = "xxx"
        self.Player = Player.Player()
        # self.enemy1 = Enemy.Enemy(screen, self.Player,self.map, "xxx")
        # self.enemy2 = EnemyMore.Devil.Devil(screen, self.Player,self.map, 300, 300, "xxx")

        self.enemyList = []

        self.mapLoader = Maploader.Maploader(screen, self.Player)

        self.rayCasting = RayCasting.RayCasting(screen)
        self.oldMouse = 0
        self.MouseSensitivity = 0.8
        self.pointer = "xxx"

    def update(self):
        for i in self.enemyList:
            i.update()
        # self.enemy1.update()
        # self.enemy2.update()
        self.Player.inputMove(self.enemyList)

   
        
    def initGame(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mapLoader.loadFile()

        # self.enemy1.image = pygame.image.load("Doom\picture\obamaFix.PNG").convert_alpha()
        self.pointer = pygame.image.load("Doom\picture\point.PNG").convert_alpha()

        self.newLevel()

    def newLevel(self):
        #if = [] -> level1
        #then next level
        if self.map == "xxx":
            self.map, self.enemyList = self.mapLoader.loadRoomEnemy("level_1")
            self.Player.map = self.map
        else:
            self.map, self.enemyList = self.mapLoader.loadRoomEnemy(self.mapLoader.nextLevel)
            self.Player.map = self.map
    def main(self):
        self.initGame()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            self.update()

            # print(self.Player.x / self.map.space, self.Player.y/ self.map.space)
            # print(self.Player.angleL, self.Player.angleR)

            screen.fill((0, 0, 0))
            
            self.rayCasting.drawRays(self.Player, self.map)
            for i in self.enemyList:
                i.render(self.rayCasting.depthList)
            # self.enemy1.render(self.rayCasting.depthList)
            # self.enemy2.render(self.rayCasting.depthList)
            self.map.drawMinimap(screen, self.Player, self.enemyList)

            scaledPointer = pygame.transform.scale(self.pointer, (500,500))
            screen.blit(scaledPointer,(Constant.WIDTH // 2, 0))
            self.oldMouse = pygame.mouse.get_pos()

            for e in self.enemyList:
                if e.health == 0:
                    self.enemyList.remove(e)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
