#zhonglin
#2025 05 23

import pygame
import math
import numpy

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
                    [1,1,1,1,1,1,1,1]]
        self.space = 60
        self.width = len(self.map[0])
        self.height = len(self.map)
    
    def getmap(self):
        return self.map


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

        self.angleL = self.angle - (self.fieldOfView //2)
        self.angleR = self.angle + (self.fieldOfView //2)


class enemy:
    #this is going to be a line 
    def __init__(self,player, width):
        self.player = player
        #this is the starting point
        self.x = 0
        self.y = 0
        #direction of the end point, always 90 to player, for cover check
        self.angle = 0
        #end point
        self.endx = self.x + width * math.cos(self.angle)
        self.endy = self.y + width * math.sin(self.angle)
        #screen point(top right, for picture)
        self.screenX = 0
        self.screenY = 0

    #did the line of view cross the line for enemy 


    def upDate(self):
        self.angle = math.atan2( self.player.y - self.y, self.player.x-self.x)


class RayCasting():
    def __init__(self):
        self.checkList = [] #a list of object that have a function that return a list of points


    #the point is clock side, check the cross product of each side, 
    def isInShape(self, point, listOfPoint):
        pass

    def addItem(self,thing):
        ''' 
        thing should have x,y, and endx, endy
        '''
        self.checkList.append(thing)

    
    def getDep(self, angle, map, Player):
        depth = 0
        xcomp =  math.cos(math.radians(angle))
        ycomp = math.sin(math.radians(angle))

        RangeOfAngleForE = []


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
            
    def didLineCross(self,startLine1, endLine1, startLine2, endLine2):
        '''line1 should be you view, line2 should be enemy'''
        l2 = [endLine2[0] - startLine2[0], endLine2[1] - startLine2[1]]
        l1 = [endLine1[0] - startLine1[0], endLine1[1] - startLine1[1]]
        #line1 as base
        s1s2 = [startLine2[0] - startLine1[0],startLine2[1] - startLine1[1]]
        s1e2 = [endLine2[0] - startLine1[0], endLine2[1] - startLine1[1]]

        l2CrossL1 = numpy.linalg.det(l1, s1s2) * numpy.linalg.det(l1, s1e2) <=0
        
        #line2 as base
        s2s1 = [startLine1[0] - startLine2[0], startLine1[1] - startLine2[1]]
        s2e1 = [endLine1[0] - startLine2[0], endLine1[0] - startLine2[0]]

        l1CrossL2 = numpy.linalg.det(l2, s2s1) * numpy.linalg.det(l2, s2e1) <= 0
        
        return l2CrossL1 and l1CrossL2
    
    def didHitLine(self, startLine1, endLine1, startLine2, endLine2):
        '''use when find depth of enemy, field of view check make sure they cross, 
        l1 is you view, l2 is enemy, this used to find did l2 cut between l1'''
        l2 = [endLine2[0] - startLine2[0], endLine2[1] - startLine2[1]]

        s2s1 = [startLine1[0] - startLine2[0], startLine1[1] - startLine2[1]]
        s2e1 = [endLine1[0] - startLine2[0], endLine1[0] - startLine2[0]]

        return numpy.linalg.det(l2, s2s1) * numpy.linalg.det(l2, s2e1) <= 0
        
   
    #???
    def quickCheck(self, startLine1, endLine1, startLine2, endLine2):
        xxx = max(startLine1[0], endLine1[0]) < max(startLine2[0], endLine2[0])
        yyy = max(startLine1[1], endLine1[1]) < max(startLine2[1], endLine2[1])
        return not xxx and not yyy
    
class Game:
    def __init__(self):
        self.map = Map()
        self.Player = Player(self.map)
        self.enemy1 = enemy(self.Player, 60)
        self.rayCasting = RayCasting()
        self.oldMouse = 0
        self.MouseSensitivity = 0.8

    def update(self):
        self.enemy1.upDate()
        self.Player.inputMove()
        
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
                

            self.update()

            print(self.Player.x / self.map.space, self.Player.y/ self.map.space)

            screen.fill((0, 0, 0))
            self.rayCasting.drawRays(self.Player, self.map)

            self.oldMouse = pygame.mouse.get_pos()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
game = Game()
game.main()    
