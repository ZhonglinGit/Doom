#zhonglin
#2025 05 23

import pygame
import math


pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Map():
    def __init__(self):
        
        self.map = [[1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,1],
                    [1,0,1,0,0,1,0,1],
                    [1,0,0,0,0,0,0,1],
                    [1,0,1,0,0,0,1,1],
                    [1,0,1,0,0,0,1,1],
                    [1,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1],]
        self.space = 60
        self.width = len(self.map[0])
        self.height = len(self.map)
    
    def getmap(self):
        return self.map



class player():

    def __init__(self):
        self.x = 4 * 30
        self.y = 4 * 30
        self.angle = 0
        self.viewDis = 360
        self.fieldOfView = 60  # degrees
        self.deltaAngle = self.fieldOfView / WIDTH  # degrees per ray
        self.speed =  3
        self.Aspeed = 2


class Game:
    def __init__(self):
        self.map = Map()
        self.player = player()
        self.oldMouse = 0
        self.MouseSensitivity = 0.8

    
    def getDelPos(self, oldPos):
        pos = pygame.mouse.get_pos()
        delPos = (pos[0] - oldPos)*0.5
        self.delPos = delPos
        return delPos
    def getDep(self, angle, map, player):
        xcomp =  math.cos(math.radians(angle))
        ycomp = math.sin(math.radians(angle))

        for i in range(1, player.viewDis + 1):
            x = player.x + i * xcomp
            y = player.y + i * ycomp

            mapX = int(x / map.space)
            mapY = int(y / map.space)


            if map.map[mapY][mapX] == 1:
                return i
        return player.viewDis

    def drawRays(self, player, map):
        startA = player.angle - player.fieldOfView / 2
        for i in range(WIDTH):
            angle = startA + i * player.deltaAngle
            depth = self.getDep(angle, map, player)
            depth *= math.cos(math.radians(angle - player.angle))  # Correct for fish-eye effect
            wallH = 21000 / depth
            color = -(255 / player.viewDis) * depth + 255
            pygame.draw.line(screen, (color, 0, 0), 
                            (i, HEIGHT // 2 - wallH // 2),#start point(top)
                                (i, HEIGHT // 2 + wallH // 2))#end of line
        
    def canYouMove(self, x, y):
        mapX = int(x / self.map.space)
        mapY = int(y / self.map.space)
        
      
        if self.map.map[mapY][mapX] == 1:
            return False

        return True

        
    def inputMove(self):
            keys = pygame.key.get_pressed()
            dx = self.player.speed * math.cos(math.radians(self.player.angle)) # back and forth movement
            dy = self.player.speed * math.sin(math.radians(self.player.angle))

            # for move side way
            dRightX = self.player.speed * math.cos(math.radians(self.player.angle + 90))
            dRightY = self.player.speed * math.sin(math.radians(self.player.angle + 90))

            # back
            if keys[pygame.K_s]:
                self.player.x -= dx
                # if you run in to a wall, undo the move
                if not self.canYouMove(self.player.x,self.player.y ):
                    self.player.x += dx
                
                self.player.y -= dy
                if not self.canYouMove(self.player.x,self.player.y ):
                    self.player.y += dy


            # forward
            if keys[pygame.K_w]:

                self.player.x += dx
                if not self.canYouMove(self.player.x,self.player.y ):
                    self.player.x -= dx

                self.player.y += dy
                if not self.canYouMove(self.player.x,self.player.y ):
                    self.player.y -= dy


            if keys[pygame.K_d]:
                # y 
                self.player.y += dRightY
                if not self.canYouMove(self.player.x, self.player.y):
                    self.player.y -= dRightY
 
                # x
                self.player.x += dRightX
                if not self.canYouMove(self.player.x, self.player.y):
                    self.player.x -= dRightX

            if keys[pygame.K_a]:
                #y
                self.player.y -= dRightY
                if not self.canYouMove(self.player.x, self.player.y):
                    self.player.y += dRightY

                #X
                self.player.x -= dRightX
                if not self.canYouMove(self.player.x, self.player.y):
                    self.player.x += dRightX

            deltaPos =  pygame.mouse.get_rel()[0] 

            self.player.angle += deltaPos
            if keys[pygame.K_i]:
                self.player.angle -= self.player.Aspeed
            if keys[pygame.K_p]:
                self.player.angle += self.player.Aspeed
    def main(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                

            self.inputMove()

            print(self.player.x / self.map.space, self.player.y/ self.map.space)

            screen.fill((0, 0, 0))
            self.drawRays(self.player, self.map)

            self.oldMouse = pygame.mouse.get_pos()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
