
import math
import sympy
import numpy
import pygame

WIDTH, HEIGHT = 640, 480

class RayCasting():
    def __init__(self, screen):
        self.checkList = {} #a list of object that have a function that return a list of points
        self.screen = screen
        self.depthList = []

    #the point is clock side, check the cross product of each side, 
    def isInShape(self, point, listOfPoint):
        pass

    def addItem(self,thing):
        ''' 
        thing should have x,y, and endx, endy
        '''
        self.checkList[thing.name] = thing

    def getCoincide(self, player):
        listRangeToCheck = []
        for name, enemy in self.checkList.items():
            #make sure you start from the small num 
            enemyAngleRange = sorted([enemy.anglePtoStart, enemy.anglePtoEnd])
            playerFov = sorted([player.angleL, player.angleR])

            #find the range
            startAngle = max(enemyAngleRange[0],playerFov[0])
            endAngle = min(enemyAngleRange[1], playerFov[1])

            if startAngle <= endAngle:
                listRangeToCheck.append([startAngle, endAngle, name])

        return listRangeToCheck
                             
    
    def getDep(self, angle, map, player):
        xcomp =  math.cos(math.radians(angle))
        ycomp = math.sin(math.radians(angle))

        enemyThere = False
        enemyGetHit = ""

        # for future if I go different type of enemy
        # for rangeOfA in RangeOfAngleForE:
        #     if angle <= rangeOfA[1] and angle >= rangeOfA[0]:
        #         enemyGetHit = self.checkList[rangeOfA[2]]
        #         enemyThere = True
        #         break


        for i in range(1, player.viewDis + 1):
            x = player.x + i * xcomp
            y = player.y + i * ycomp

            mapX = int(x / map.space)
            mapY = int(y / map.space)

            # #remove this part
            # if enemyThere:
            #     if self.didHitLine([player.x, player.y], [x, y], [enemyGetHit.x, enemyGetHit.y], [enemyGetHit.endx, enemyGetHit.endy]):
            #         return [i, enemyGetHit.color]

            if map.map[mapY][mapX] == 1:
                return [i, map.color]
                
        return [player.viewDis, (0,0,0)]


    def drawRays(self, player, map):
        startA = player.angle - player.fieldOfView / 2
        # RangeOfAngleForE = self.getCoincide(player)
        # a function in enemy called draw here
        for i in range(WIDTH):
            angle = startA + i * player.deltaAngle
            depth = self.getDep(angle, map, player)
            depth[0] *= math.cos(math.radians(angle - player.angle))  # Correct for fish-eye effect, can optomoze
            self.depthList.append(depth[0])
            wallH = 21000 / depth[0]

            color1 = -(depth[1][0] / player.viewDis) * depth[0] + depth[1][0]
            color2 = -(depth[1][1] / player.viewDis) * depth[0] + depth[1][1]
            color3 = -(depth[1][2] / player.viewDis) * depth[0] + depth[1][2]

            pygame.draw.line(self.screen, (color1, color2, color3), 
                            (i, HEIGHT // 2 - wallH // 2),#start point(top)
                                (i, HEIGHT // 2 + wallH // 2))#end of line
            
    def didLineCross(startLine1, endLine1, startLine2, endLine2):
        l2 = [endLine2[0] - startLine2[0], endLine2[1] - startLine2[1]]
        l1 = [endLine1[0] - startLine1[0], endLine1[1] - startLine1[1]]
        #line1 as base
        s1s2 = [startLine2[0] - startLine1[0],startLine2[1] - startLine1[1]]
        s1e2 = [endLine2[0] - startLine1[0], endLine2[1] - startLine1[1]]

        l2CrossL1 = numpy.linalg.det(numpy.array([l1, s1s2])) * numpy.linalg.det(numpy.array([l1, s1e2])) <=0
        
        #line2 as base
        s2s1 = [startLine1[0] - startLine2[0], startLine1[1] - startLine2[1]]
        s2e1 = [endLine1[0] - startLine2[0], endLine1[1] - startLine2[1]]

        l1CrossL2 = numpy.linalg.det(numpy.array([l2, s2s1])) * numpy.linalg.det(numpy.array([l2, s2e1])) <= 0
        
        return l2CrossL1 and l1CrossL2
    
    def didHitLine(self, startLine1, endLine1, startLine2, endLine2):
        '''use when find depth of enemy, field of view check make sure they cross, 
        l1 is you view, l2 is enemy, this used to find did l2 cut between l1'''
        l2 = [endLine2[0] - startLine2[0], endLine2[1] - startLine2[1]]

        s2s1 = [startLine1[0] - startLine2[0], startLine1[1] - startLine2[1]]
        s2e1 = [endLine1[0] - startLine2[0], endLine1[1] - startLine2[1]]

        return  numpy.linalg.det(numpy.array([l2, s2s1])) * numpy.linalg.det(numpy.array([l2, s2e1])) <= 0
        
   
    #???
    def quickCheck(self, startLine1, endLine1, startLine2, endLine2):
        xxx = max(startLine1[0], endLine1[0]) < max(startLine2[0], endLine2[0])
        yyy = max(startLine1[1], endLine1[1]) < max(startLine2[1], endLine2[1])
        return not xxx and not yyy