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
        self.map = Map()
        self.Player = Player.Player(self.map)
        self.enemy1 = Enemy.Enemy(screen, self.Player,self.map, "xxx")
        self.enemy2 = EnemyMore.Devil.Devil(screen, self.Player,self.map, 300, 300, "xxx")

        self.enemyList = []

        self.mapLoader = Maploader.Maploader(screen, self.Player)

        

        self.rayCasting = RayCasting.RayCasting(screen)
        self.oldMouse = 0
        self.MouseSensitivity = 0.8
        self.pointer = "xxx"

    def update(self):
        self.enemy1.update()
        self.enemy2.update()
        self.Player.inputMove(self.enemy1)

    def drawMinimap(self, surface):
        scale = 0.15
        scaleSize = int(self.map.space * scale)
        
        # walls
        #enumerate help you get the index when you go through a list
        for y, row in enumerate(self.map.map):
            for x, v in enumerate(row):
                color = (30, 30, 30)
                if v == 1:
                    color = (200, 200, 200)
                pygame.draw.rect(surface, color, pygame.Rect(
                    x * scaleSize, y * scaleSize, scaleSize, scaleSize
                ))

        # player
        px = self.Player.x * scale
        py = self.Player.y * scale
        pygame.draw.circle(surface, (0, 255, 0), (int(px), int(py)), 3)

        # angle
        dx = math.cos(math.radians(self.Player.angle)) * 10
        dy = math.sin(math.radians(self.Player.angle)) * 10
        pygame.draw.line(surface, (0, 255, 0), (px, py), (px + dx, py + dy), 2)

        # enemy
        ex = self.enemy1.midX * scale
        ey = self.enemy1.midY * scale
        ew = self.enemy1.width * scale / 2
        ex1 = ex - ew * math.cos(math.radians(self.enemy1.angle))
        ey1 = ey - ew * math.sin(math.radians(self.enemy1.angle))
        ex2 = ex + ew * math.cos(math.radians(self.enemy1.angle))
        ey2 = ey + ew * math.sin(math.radians(self.enemy1.angle))

        pygame.draw.line(surface, (255, 0, 0), (ex1, ey1), (ex2, ey2), 2)

        
    def initGame(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mapLoader.loadFile()

        self.enemy1.image = pygame.image.load("Doom\picture\obamaFix.PNG").convert_alpha()
        self.pointer = pygame.image.load("Doom\picture\point.PNG").convert_alpha()

        self.newLevel()

    def newLevel(self):
        #if = [] -> level1
        #then next level
        if self.map.map == []:
            self.map.map, self.enemyList = self.mapLoader.loadRoomEnemy("level_1")
        else:
            self.map.map, self.enemyList = self.mapLoader.loadRoomEnemy(self.mapLoader.nextLevel)
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
            self.enemy1.render(self.rayCasting.depthList)
            self.enemy2.render(self.rayCasting.depthList)
            self.drawMinimap(screen)

            scaledPointer = pygame.transform.scale(self.pointer, (500,500))
            screen.blit(scaledPointer,(Constant.WIDTH // 2, 0))
            self.oldMouse = pygame.mouse.get_pos()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
