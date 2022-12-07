import random

class Player():
    def __init__(self, xpos, ypos, charrunning, charjumping, upsidedownrun):
        self.xpos = xpos
        self.ypos = ypos
        self.charrunning = charrunning
        self.charjumping = charjumping
        self.upsidedownrun = upsidedownrun
        self.image = self.charrunning[0] 
        self.dyingFrame = -1
        self.isdown = True
        self.isup = False
        self.lives = [True, True, True]
        self.invincible = False
    
    def isStanding(self):
        self.image = self.charrunning[0]
    
    def isRunning(self, dx, frame):
        charsList = copy.copy(self.charrunning)
        charsList.pop(0)
        self.xpos += dx
        self.image = charsList[frame]
        self.isdown = True
        self.isup = False
    
    def upsideDownRunning(self, dx, frame):
        charsList = copy.copy(self.upsidedownrun)
        charsList.pop(0)
        self.xpos += dx
        self.image = charsList[frame]
        self.isdown = False
        self.isup = True
    
    def isJumping(self, dx, frame):
        self.xpos += dx*1.3
        if self.ypos >= 187:
            self.ypos -= 35
            self.image = self.charjumping[frame]
            if self.image == self.charjumping[-2]:
                self.image = self.charjumping[-1]
        self.isup = True
        self.isdown = False
    
    def isDownJump(self, dx, frame):
        self.xpos += dx*1.5
        if self.ypos < 385:
            self.ypos += 35
            self.image = self.charjumping[frame]
        self.isdown = True
        self.isup = False

    def died(self, obstacle):
        if self.invincible == True:
            return False
        if self.isup and obstacle.isup:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
        if self.isdown and obstacle.isdown:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
    
    def killYourself(self, x, y, animation, height):
        self.xpos = x
        self.ypos = y
        
        self.image = animation[0]
        if self.dyingFrame < 10:
                self.image = animation[self.dyingFrame//2]
                self.dyingFrame += 1
        else:
            self.image = animation[5]
                
    def restart(self, collidedobstacle): 
        self.xpos = collidedobstacle.xpos - 200 #app width
        self.ypos = 532*4/5 - 40 #app.height
        self.image = self.charrunning[0]

  
#backtracking              
def isLegal(obstacles, player): #self, xpos, ypos, width, height
    if len(obstacles) == 1:
        return True
    else:
        for element in obstacles:
            if element.xpos <= player.xpos and player.xpos <= element.xpos + element.width * 24:
                return False
        for element1 in obstacles:
            for element2 in obstacles:
                if element1 != element2:
                    if element2.enoughDistance(element1) == False:
                        return False
        return True

def placeObstacles(obstacles, level, screenstart, screenwidth, player):
    if level == 0:
        return obstacles
    else:
        ypos = random.randint(0, 1)
        if ypos == 0:
            ypos = 532 * 4/5 - 24 #isdown
        if ypos == 1:
            ypos = 532/4 + 24 #isup
        
        if obstacles == []:
            insert = Obstacle(random.randint(screenstart, screenwidth), ypos, random.randint(2, 4), random.randint(2, 6)) 
        else:
            start = obstacles[-1].xpos + (obstacles[-1].width + 2) * 24
            insert = Obstacle(random.randint(start, int(start + screenwidth/8)), ypos, random.randint(2,4), random.randint(2,6))
        
        obstacles.append(insert)
        
        if isLegal(obstacles, player):
            solution = placeObstacles(obstacles, level - 1, screenstart, screenwidth, player)
            if solution != None:
                return solution
            else:
                obstacles.remove(insert)
                
        return None
    
class Obstacle():
    def __init__(self, xpos, ypos, width, height):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        if self.ypos == 532 * 4/5 - 24:
            self.isup = False
            self.isdown = True
        if self.ypos == 532/4 + 24:
            self.isup = True
            self.isdown = False
        self.start = self.xpos
        self.end = self.xpos + self.width * 24
    
    def drawObstacle(self, canvas, image, scrollX):
        if self.isdown == True:
            for j in range(self.height):
                for i in range(self.width):
                    canvas.create_image(self.xpos + i*24 - scrollX, self.ypos - j*24, image=ImageTk.PhotoImage(image))
        if self.isup == True:
            for j in range(self.height):
                for i in range(self.width):
                    canvas.create_image(self.xpos + i*24 - scrollX, self.ypos + j*24, image = ImageTk.PhotoImage(image))

    def __hash__(self):
        return(hash((self.xpos, self.ypos)))
    
    def __eq__(self, other):
        if type(other) != Obstacle:
            return False
        else:
            if self.xpos == other.xpos and self.ypos == other.ypos:
                return True
    def __repr__(self):
        return f"Obstacle: {self.xpos, self.ypos}"
            
    #checks if there's enough space between two obstacles for the character to pass through them
    def enoughDistance(self, other):
        selfrange = range(self.xpos - (10*24), self.xpos + (self.width+10)*24)
        otherrange = range(other.xpos - (10*24), other.xpos + (other.width+10)*24)
        
        selfrange = set(selfrange)
        otherrange = set(otherrange)
        
        intersect = selfrange & otherrange

        if intersect != set():
            return False
        return True
    
class Star():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.width = 2
        if self.ypos == 532 * 4/5 - 24:
            self.isup = False
            self.isdown = True
        if self.ypos == 532/4 + 24:
            self.isup = True
            self.isdown = False
    
    def isTouchingPlayer(self, player):
        if player.isup and self.isup:
            if player.xpos > self.xpos and player.xpos < self.xpos + self.width * 24:
                return True
        if player.isdown and self.isdown:
            if player.xpos > self.xpos and player.xpos < self.xpos + self.width * 24:
                return True
    
    def isTouchingObstacle(self, obstacle):
        if self.isup and obstacle.isup:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
        if self.isdown and obstacle.isdown:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
    
    #recursive placing star homemade algorithm  
    def placeStar(self, player, width, obstacles):
        self.xpos = random.randint(int(player.xpos + 400), int(player.xpos + width))
        for obstacle in obstacles:
            if self.isTouchingObstacle(obstacle):
                self.placeStar(player, width, obstacles)
        return True
    
    def drawStar(self, canvas, image, scrollX):
        canvas.create_image(self.xpos - scrollX, self.ypos, image = ImageTk.PhotoImage(image))