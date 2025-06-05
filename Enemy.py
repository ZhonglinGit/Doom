import math
import sympy
import angles
import pygame

WIDTH, HEIGHT = 640, 480

class Enemy:
    def __init__(self, screen, player, width, name):
        self.screen = screen
        self.player = player
        self.name = name
        self.color = (0, 255, 0)
        self.width = width
        self.image = "place holder"
        self.midX = 240
        self.midY = 240
        self.x = self.y = 0
        self.endx = self.endy = 0
        self.angle = 0
        self.anglePtoStart = 0
        self.anglePtoEnd = 0

    def update(self):
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
    def didGotShot(self):
        playerEndx = self.player.x + math.cos(math.radians(self.player.angle)) * self.player.viewDis
        playerEndy = self.player.y + math.sin(math.radians(self.player.angle)) * self.player.viewDis
        #player angle line and enemy line
        p, t = self.whereTwoLineMeet((self.player.x, self.player.y), (playerEndx, playerEndy), (self.x, self.y), (self.endx, self.endy))

        if t == None:
            #didn't cross
            return False
        if 0 < t < 1:
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
        """计算从 from_angle 到 to_angle 的有向角度差（可为负数）"""
        diff = (to_angle - from_angle + 540) % 360 - 180
        return diff
    def is_angle_between(self, a, left, right):
        a %= 360
        left %= 360
        right %= 360
        if left < right:
            return left <= a <= right
        else:
            return a >= left or a <= right

    def getWhatToDesplay(self):
        viewStart = (self.player.x, self.player.y)
        viewRightEnd = (self.player.x + math.cos(self.player.angleR) * self.player.viewDis,
                        self.player.y + math.sin(self.player.angleR) * self.player.viewDis)
        viewLeftEnd = (self.player.x + math.cos(self.player.angleL) * self.player.viewDis,
                    self.player.y + math.sin(self.player.angleL) * self.player.viewDis)
        enemyPoint = (self.x, self.y)
        enemyEndPoint = (self.endx, self.endy)

        rightPoint, rightT = self.whereTwoLineMeet(viewStart, viewRightEnd, enemyPoint, enemyEndPoint)
        leftPoint, leftT = self.whereTwoLineMeet(viewStart, viewLeftEnd, enemyPoint, enemyEndPoint)

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
        
        # 情况4：都交点（正常显示）
        return int(screenx1), int(fullWidth)


    def getDisToPlayer(self):
        return math.hypot(self.midX - self.player.x, self.midY - self.player.y)

    def render(self, depthList):
        startPoint, widthRec = self.getWhatToDesplay()
        if startPoint is None:
            return
        dis = self.getDisToPlayer()
        eh = 18000 / dis
        # pygame.draw.rect(self.screen, self.color,
        #                  pygame.Rect(int(startPoint), int(HEIGHT // 2 - eh // 2), int(widthRec), int(eh)))
        
        scaled = pygame.transform.scale(self.image, (int(widthRec), int(eh)))
        self.screen.blit(scaled, (int(startPoint), int(HEIGHT // 2 - eh // 2)))
        # for x in range(int(startPoint), int(startPoint + widthRec)):
        #     if x < 0 or x >= WIDTH:
        #         continue
        #     if self.getDisToPlayer() < depthList[x]:  # 敌人比墙更近
        #         pygame.draw.line(self.screen, self.color, (x, HEIGHT//2 - eh//2), (x, HEIGHT//2 + eh//2))

