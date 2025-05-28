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


class Player():

    def __init__(self):
        self.x = 4 * 30
        self.y = 4 * 30
        self.angle = 0
        self.viewDis = 360
        self.fieldOfView = 60  # degrees
        self.deltaAngle = self.fieldOfView / WIDTH  # degrees per ray
        self.speed =  3
        self.Aspeed = 2

class enemy:
    def __init__(self):
        pass

class RayCasting():
    def __init__(self):
        self.checkList = [] #a list of object that have a function that return a list of points


    #the point is clock side, check the slope of each side, 
    def isInShape(self, point, listOfPoint):
        pass

    def getDep(self, angle, map, Player):
        xcomp =  math.cos(math.radians(angle))
        ycomp = math.sin(math.radians(angle))

        for i in range(1, Player.viewDis + 1):
            x = Player.x + i * xcomp
            y = Player.y + i * ycomp

            mapX = int(x / map.space)
            mapY = int(y / map.space)


            if map.map[mapY][mapX] == 1:
                return i
        return Player.viewDis

    def drawRays(self, Player, map):
        startA = Player.angle - Player.fieldOfView / 2
        for i in range(WIDTH):
            angle = startA + i * Player.deltaAngle
            depth = self.getDep(angle, map, Player)
            depth *= math.cos(math.radians(angle - Player.angle))  # Correct for fish-eye effect
            wallH = 21000 / depth
            color = -(255 / Player.viewDis) * depth + 255
            pygame.draw.line(screen, (color, 0, 0), 
                            (i, HEIGHT // 2 - wallH // 2),#start point(top)
                                (i, HEIGHT // 2 + wallH // 2))#end of line
class Game:
    def __init__(self):
        self.map = Map()
        self.Player = Player()
        self.rayCasting = RayCasting()
        self.oldMouse = 0
        self.MouseSensitivity = 0.8


    def canYouMove(self, x, y):
        mapX = int(x / self.map.space)
        mapY = int(y / self.map.space)
        
      
        if self.map.map[mapY][mapX] == 1:
            return False

        return True

        
    def inputMove(self):
            keys = pygame.key.get_pressed()
            dx = self.Player.speed * math.cos(math.radians(self.Player.angle)) # back and forth movement
            dy = self.Player.speed * math.sin(math.radians(self.Player.angle))

            # for move side way
            dRightX = self.Player.speed * math.cos(math.radians(self.Player.angle + 90))
            dRightY = self.Player.speed * math.sin(math.radians(self.Player.angle + 90))

            # back
            if keys[pygame.K_s]:
                self.Player.x -= dx
                # if you run in to a wall, undo the move
                if not self.canYouMove(self.Player.x,self.Player.y ):
                    self.Player.x += dx
                
                self.Player.y -= dy
                if not self.canYouMove(self.Player.x,self.Player.y ):
                    self.Player.y += dy


            # forward
            if keys[pygame.K_w]:

                self.Player.x += dx
                if not self.canYouMove(self.Player.x,self.Player.y ):
                    self.Player.x -= dx

                self.Player.y += dy
                if not self.canYouMove(self.Player.x,self.Player.y ):
                    self.Player.y -= dy


            if keys[pygame.K_d]:
                # y 
                self.Player.y += dRightY
                if not self.canYouMove(self.Player.x, self.Player.y):
                    self.Player.y -= dRightY
 
                # x
                self.Player.x += dRightX
                if not self.canYouMove(self.Player.x, self.Player.y):
                    self.Player.x -= dRightX

            if keys[pygame.K_a]:
                #y
                self.Player.y -= dRightY
                if not self.canYouMove(self.Player.x, self.Player.y):
                    self.Player.y += dRightY

                #X
                self.Player.x -= dRightX
                if not self.canYouMove(self.Player.x, self.Player.y):
                    self.Player.x += dRightX

            
            deltaPos =  pygame.mouse.get_rel()[0] 

            self.Player.angle += deltaPos
            if keys[pygame.K_i]:
                self.Player.angle -= self.Player.Aspeed
            if keys[pygame.K_p]:
                self.Player.angle += self.Player.Aspeed

            if keys[pygame.K_m]:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)

    def initGame(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    def main(self):
        self.initGame()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                

            self.inputMove()

            print(self.Player.x / self.map.space, self.Player.y/ self.map.space)

            screen.fill((0, 0, 0))
            self.rayCasting.drawRays(self.Player, self.map)

            self.oldMouse = pygame.mouse.get_pos()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
