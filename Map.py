
import math
import pygame
import Constant

class Map():
    def __init__(self, mapList):
        
        self.map = mapList
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.color = (255,0, 0)
    
    def getmap(self):
        return self.map
    def canYouMove(self, x, y):
        mapX = int(x / Constant.SPACE)
        mapY = int(y / Constant.SPACE)
        
        if mapX > self.width-1 or mapY > self.height-1:
            return True

        if self.map[mapY][mapX] == 1:
            return False

        return True
    def drawMinimap(self, screen, player, enemyList):
        scale = 0.3
        scaleSize = int(Constant.SPACE * scale)
        
        startxDis = Constant.WIDTH - self.width * scaleSize
        
        # walls
        #enumerate help you get the index when you go through a list
        for y, row in enumerate(self.map):
            for x, v in enumerate(row):
                color = (30, 30, 30)
                if v == 1:
                    color = (200, 200, 200)
                pygame.draw.rect(screen, color, pygame.Rect(
                    x * scaleSize +startxDis, y * scaleSize, scaleSize, scaleSize
                ))

        # player
        px = player.x * scale
        py = player.y * scale
        pygame.draw.circle(screen, (0, 255, 0), (int(px+startxDis), int(py)), 3)

        # angle
        dx = math.cos(math.radians(player.angle)) * 10
        dy = math.sin(math.radians(player.angle)) * 10
        pygame.draw.line(screen, (0, 255, 0), (px+startxDis, py), (px + dx+startxDis, py + dy), 2)

        # enemy
        for e in enemyList:
            ex = e.midX * scale
            ey = e.midY * scale
            ew = e.width * scale / 2
            ex1 = ex - ew * math.cos(math.radians(e.angle))
            ey1 = ey - ew * math.sin(math.radians(e.angle))
            ex2 = ex + ew * math.cos(math.radians(e.angle))
            ey2 = ey + ew * math.sin(math.radians(e.angle))

            pygame.draw.line(screen, (255, 0, 0), (ex1+startxDis, ey1), (ex2+startxDis, ey2), 2)
