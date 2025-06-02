import math
import sympy

class Enemy:
    #this is going to be a line 
    def __init__(self,player, width, name):
        self.player = player
        self.name = name
        self.color = (0,255,0)
        self.width = width
        #this is the starting point
        self.x = 240
        self.y = 240
        #middle
        self.midX = 240
        self.midY = 240

        #direction of the end point, always 90 to player, for cover check
        self.angle = 0
        #end point
        self.endx = 0
        self.endy = 0
        #screen point(top right, for picture)
        self.screenX = 0
        self.screenY = 0
        #angle from player to eney
        #for ray casting
        self.anglePtoStart = 0
        self.anglePtoEnd = 0

    def upDate(self):
        # self.angle = math.atan2( self.player.y - self.y, self.player.x-self.x)
        self.angle = self.player.angle + 90

        halfWidth = self.width / 2
        rad = math.radians(self.angle)
        self.endx = self.midX + halfWidth * math.cos(rad)
        self.endy = self.midY + halfWidth * math.sin(rad)

        self.x = self.midX - halfWidth * math.cos(rad) 
        self.y = self.midY - halfWidth * math.sin(rad)

        self.anglePtoStart = math.degrees(math.atan2(self.y - self.player.y, self.x - self.player.x))
        self.anglePtoEnd = math.degrees(math.atan2(self.endy - self.player.y, self.endx - self.player.x))


    def rander():
        t, u = sympy.symbols('t u')