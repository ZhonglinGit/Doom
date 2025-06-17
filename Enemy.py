import math
import sympy
import angles
import pygame
import Constant

WIDTH, HEIGHT = 640, 480

class Enemy:
    def __init__(self, screen, player,map, name):
        self.screen = screen
        self.player = player
        self.map = map

        self.name = name
        self.color = (0, 255, 0)
        self.width = 20
        self.image = "place holder"

        self.fullhealth = 5
        self.health = self.fullhealth

        self.midX = 240
        self.midY = 240

        #these are start point
        self.x = 0
        self.y = 0
        #these are end point
        self.endx =0
        self.endy = 0

        self.angle = 0
        self.anglePtoStart = 0
        self.anglePtoEnd = 0

        self.speed =2.5

        self.deeplist = "xxx"


    def update(self):
       
        self.health = max(0,self.health)
        self.angle = self.player.angle + 90
        halfWidth = self.width / 2
        rad = math.radians(self.angle)
        dx = halfWidth * math.cos(rad)
        dy = halfWidth * math.sin(rad)
        self.x = self.midX - dx
        self.y = self.midY - dy
        self.endx = self.midX + dx
        self.endy = self.midY + dy
        self.anglePtoStart = angles.normalize(math.degrees(math.atan2(self.y - self.player.y, self.x - self.player.x)))
        self.anglePtoEnd = angles.normalize(math.degrees(math.atan2(self.endy - self.player.y, self.endx - self.player.x)))

        
        if self.getDisToPlayer() < 10:
            self.player.getHit()
        

    def didGotShot(self, damage):
        playerEndx = self.player.x + math.cos(math.radians(self.player.angle)) * self.player.viewDis
        playerEndy = self.player.y + math.sin(math.radians(self.player.angle)) * self.player.viewDis
        #player angle line and enemy line
        p, t = self.whereTwoLineMeet((self.player.x, self.player.y), (playerEndx, playerEndy), (self.x, self.y), (self.endx, self.endy))

        if t == None:
            #didn't cross
            return False
        
        dis = math.hypot(p[0] - self.player.x, p[1] - self.player.y)
        if dis > self.deeplist[Constant.WIDTH //2-1]:
            #you don't shot through wall only need to check the mid line
            return False
        
        if 0 < t < 1:
            self.health -= damage
            return True
        return False

    def whereTwoLineMeet(self, a, b, c, d):
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d
        r_px = bx - ax
        r_py = by - ay
        s_px = dx - cx
        s_py = dy - cy
        denom = r_px * s_py - r_py * s_px
        if denom == 0:
            return None, None
        u = ((cx - ax) * s_py - (cy - ay) * s_px) / denom
        t = ((cx - ax) * r_py - (cy - ay) * r_px) / denom
        if u >= 0 and 0 <= t <= 1:
            ix = ax + r_px * u
            iy = ay + r_py * u
            return (ix, iy), t
        else:
            return None, None

    def relative_angle_diff(self, from_angle, to_angle):
        """get the angle between the two, 180 to -180, so it kind of have direction"""
        diff = (to_angle - from_angle + 540) % 360 - 180
        return diff
    def is_angle_between(self, a, left, right):
        """check is a between left and right, consider over 360"""
        a %= 360
        left %= 360
        right %= 360
        if left < right:
            return left <= a <= right
        else:
            return a >= left or a <= right

    def getWhatToDesplay(self):

        leftAngle  = self.relative_angle_diff(self.player.angleL, self.anglePtoStart)
        rightAngle = self.relative_angle_diff(self.player.angleL, self.anglePtoEnd)

        # get the angle and get the transform 
        sx1 = self.relative_angle_diff(self.player.angleL, self.anglePtoStart) / self.player.deltaAngle
        sx2 = self.relative_angle_diff(self.player.angleL, self.anglePtoEnd) / self.player.deltaAngle
        screenx1 = min(sx1, sx2)
        screenx2 = max(sx1, sx2)
        fullWidth = screenx2 - screenx1

        # print(self.relative_angle_diff(self.player.angleL, self.anglePtoStart), self.relative_angle_diff(self.player.angleL, self.anglePtoEnd))

        if leftAngle * rightAngle <= 0 and abs(leftAngle)>90 and abs(rightAngle) >90:
            return None, None
        
        return int(screenx1), int(fullWidth)


    def getDisToPlayer(self):
        return math.hypot(self.midX - self.player.x, self.midY - self.player.y)

    def render(self, depthList):
        self.deeplist = depthList
        startPoint, widthRec = self.getWhatToDesplay()
        if startPoint is None:
            return
        dis = self.getDisToPlayer()
        eh = 18000 / (dis +1)
        #for future
        # pygame.draw.rect(self.screen, self.color,
        #                  pygame.Rect(int(startPoint), int(HEIGHT // 2 - eh // 2), int(widthRec), int(eh)))
        

        #from 1 to viewDis, alph is 0 to 255
        alph =int(dis * -255/self.player.viewDis +255)
        #scaled the image to the right size
        scaled = pygame.transform.scale(self.image, (int(widthRec), int(eh)))
        scaled.set_alpha(alph)
        # print(alph)
        # self.screen.blit(scaled, (int(startPoint), int(HEIGHT // 2 - eh // 2)))

        #health bar
        healthSurface = pygame.Surface((int(widthRec * max(0,self.health) / self.fullhealth), int(eh * 0.05)), pygame.SRCALPHA)
        healthSurface.set_alpha(alph)
        pygame.draw.rect(healthSurface, (0, 255,0), healthSurface.get_rect())
        self.screen.blit(healthSurface, (int(startPoint), int(HEIGHT // 2 - eh // 2 - eh * 0.05)))

        for i in range(widthRec):
            x = startPoint + i
            if 0 <= x <= Constant.WIDTH:
                if dis < depthList[x-1]:
                    #cut the line on the picture
                    column = scaled.subsurface(pygame.Rect(i, 0, 1, int(eh)))
                    self.screen.blit(column, (x, HEIGHT // 2 - int(eh) // 2))

