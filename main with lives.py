from cmu_112_graphics import *
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
        if self.isup and obstacle.isup:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
        if self.isdown and obstacle.isdown:
            if self.xpos > obstacle.xpos and self.xpos < obstacle.xpos + obstacle.width * 24:
                return True
    
    def killYourself(self, x, y,animation, height):
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
            insert = Obstacle(random.randint(screenstart, screenwidth), ypos, random.randint(1, 4), random.randint(1, 6)) 
        else:
            start = obstacles[-1].xpos + (obstacles[-1].width + 2) * 24
            insert = Obstacle(random.randint(start, int(start + screenwidth/8)), ypos, random.randint(1,4), random.randint(1,6))
        
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
        
        # if self.xpos in range(other.xpos - (10*24), other.xpos + (other.width+10)*24):
        #     return False
        # if self.xpos + self.width * 24 in range(other.xpos - (10*24), other.xpos + (other.width+10)*24):
        #     return False
        # if other.xpos in range(self.xpos - 240, self.xpos + (self.width+10)*24):
        #     return False
        # if other.xpos + other.width * 24 in range(self.xpos - 240, self.xpos + (self.width+10)*24):
        #     return False
        # if self.ypos == other.ypos:
        #     if other.xpos + (15*24) < self.xpos and self.xpos < other.xpos + (other.width+15) * 24: #this controls the distance between the obstacles (the 5)
        #         return False
        # return True
    
#checks if app.player.lives is all False
def isActuallyDead(player):
    for life in player.lives:
        if life == True:
            return False
    return True
        
def appStarted(app):
    app.timerDelay = 1
    app.timerCounter = 0
    app.level = 4
    
    #background
    app.bg = app.loadImage("Images/bg1.png")
    app.posX1 = app.width/2
    app.posX2 = app.width/2 * 3
    app.scrollX = 0
    
    #terrain
    app.ogtiles = app.loadImage("Images/tiles.png")
    app.tiles = app.scaleImage(app.ogtiles, 1/3)
    app.xpos = 12
    
    #creation of the app.charrunning list for running animation
    app.ogcharstrip = app.loadImage("Images/running.png")
    app.charstrip = app.scaleImage(app.ogcharstrip, 1/2)
    app.ogstanding = app.loadImage("Images/standing.png")
    app.standing = app.scaleImage(app.ogstanding, 1/2) 
    app.charrunning = [app.standing]
    for i in range(6):
        char = app.charstrip.crop((i*55, 0, 55*(i+1), 65))
        app.charrunning.append(char)
    app.charcopy = copy.copy(app.charrunning)
    for i in range(6):
        app.charrunning.append(app.charcopy[5-i])    
    
    #!app.charrunning is the list of character frames for running animation

    #creation of app.charjumping list for jumping animation
    app.ogjumplist = app.loadImage("Images/startjump.png")
    app.jumplist = app.scaleImage(app.ogjumplist, 1/2)
    app.charjumping = []
    for i in range(3):
        char = app.charstrip.crop((i*55, 0, 55*(i+1), 65))
        app.charjumping.append(char)
    app.ogmidjump = app.loadImage("Images/midjump.png")
    app.midjump = app.scaleImage(app.ogmidjump, 1/2)
    app.ogmidjump2 = app.loadImage("Images/midjump2.png")
    app.midjump2 = app.scaleImage(app.ogmidjump2, 1/2)
    app.oglast = app.loadImage("Images/lastjumpframe.png")
    app.last = app.scaleImage(app.oglast, 1/2)
    app.down = app.standing.transpose(Image.FLIP_TOP_BOTTOM)
    app.charjumping.extend([app.midjump, app.midjump2, app.last, app.down])
    
    #! app.charjumping is the list of characters for the jumping animation, including app.standing
    
    #creation of app.upsidedownrunning which is the character running upside down
    app.upsidedownrunning = []
    for frame in app.charrunning:
        insertframe = frame.transpose(Image.FLIP_TOP_BOTTOM)
        app.upsidedownrunning.append(insertframe)
    
    #creation of dying animation
    app.dyinganimation = []
    app.ogdying = app.loadImage("Images/dyinganimation.png")
    app.dying = app.scaleImage(app.ogdying, 1/2)
    for i in range(5):
        char = app.dying.crop((i*75, 0, 75*(i+1), 54))
        app.dyinganimation.append(char)
    app.empty = app.loadImage("Images/empty.png")
    app.dyinganimation.append(app.empty)
    
    #player
    app.player = Player(app.width/4, app.height*4/5 - 40, 
                        app.charrunning, app.charjumping, 
                        app.upsidedownrunning)
    app.standing = True
    app.running = False
    app.jumping = False
    app.isAbove = False
    app.isBelow = True
    app.isDead = False
    
    #obstacle
    app.obstacles = []
    placeObstacles(app.obstacles, app.level, app.player.xpos + 400, app.width, app.player)
    app.collidedobstacle = None
    
    #lives
    app.ogfullheart = app.loadImage("Images/fullheart.png")
    app.fullheart = app.scaleImage(app.ogfullheart, 1/4)
    app.ogemptyheart = app.loadImage("Images/emptyheart.png")
    app.emptyheart = app.scaleImage(app.ogemptyheart, 1/4)
    
def timerFired(app):
    app.timerCounter += 1
    x = app.player.xpos
    y = app.player.ypos
    
    #check if player has died
    if len(app.obstacles) != 0:
        for obstacle in app.obstacles:
            if app.player.died(obstacle):
                app.running = False
                app.standing = True
                app.isDead = True
                app.collidedobstacle = obstacle
    
    #background 
    if app.isDead == False:
        app.scrollX += 10
    if app.width/2 + app.posX1 - app.scrollX <= 0:
        app.posX1 += app.width * 2 
        
    if app.width/2 + app.posX2 - app.scrollX <= 0:
        app.posX2 += app.width * 2
        
    #obstacles
    if app.timerCounter % 10 == 0:
        placeObstacles(app.obstacles, app.level, int(app.player.xpos) + 400, int(app.player.xpos) + app.width, app.player)
    
    for obstacle in app.obstacles:
        if obstacle.xpos + obstacle.width * 24 - app.scrollX < 0:
            app.obstacles.remove(obstacle)
    
    #terrain
    if app.xpos + 24 * (int(app.width/24)-1) - app.scrollX <= 0:
        app.xpos += app.width
    
    #player
    #! the variable dx is initialized here, the first variable of app.player.isRunning
    if app.running == True and app.isBelow == True:
        app.player.isRunning(10.5, app.timerCounter % 6)
    if app.running == True and app.isAbove == True:
        app.player.upsideDownRunning(10.5, app.timerCounter % 6)
    if app.standing == True and app.isBelow == True:
        app.player.isStanding()
    if app.standing == True and app.isAbove == True:
        app.player.image = app.down
    if app.jumping == True and app.isBelow == True:
        if app.player.ypos >= 187:
            app.player.isJumping(10.5, app.timerCounter % 6)
        if app.player.ypos <= 187:
            app.jumping = False
            app.isBelow = False
            app.isAbove = True
    if app.jumping == True and app.isAbove == True:
        if app.player.ypos < 385:
            app.player.isDownJump(10.5, -1 * app.timerCounter % 6)
        if app.player.ypos >= 385:
            app.jumping = False
            app.isBelow = True
            app.isAbove = False
            
    if app.standing == True and app.isDead and isActuallyDead(app.player):
        app.player.killYourself(x,y, app.dyinganimation, app.height)
        
    if app.standing == True and app.isDead == True and (isActuallyDead(app.player) == False):
        app.isAbove = False
        app.isBelow = True
        app.player.restart(app.collidedobstacle)
        
        if app.player.image == app.charrunning[0]: #! THIS ONLY WORKS IF YOU GET IT TO RESTART IN THE FIRST PLACE
            app.player.lives.pop(0)
            app.player.lives.append(False)
        app.isDead = False
        
    if isActuallyDead(app.player) == True:
        app.isDead = True
    
    # if app.player.image == app.dyinganimation[-1]:
    #     app.player.lives.pop(0)
    #     app.player.lives.append(False)
    # THIS IS ALL COMMENTED OUT CUZ YOU HAVE TO MAKE THE ANIMATION FOR IT JUST LOSING A LIFE NOT JUST DYING

def keyPressed(app, event):
    if app.isDead == False:
        if (event.key == "Right"):
            app.standing = False
            app.running = True
        if (event.key == "Up"):
            app.standing = True
            app.running = False
            app.jumping = True
        if (event.key == "Down"):
            app.standing = True
            app.running = False
            app.jumping = True
    
def redrawAll(app, canvas):
    #background
    canvas.create_image(app.posX1 - app.scrollX, app.height/2, image=ImageTk.PhotoImage(app.bg))
    canvas.create_image(app.posX2 - app.scrollX, app.height/2, image=ImageTk.PhotoImage(app.bg))
    
    #terrain
    for i in range(int(app.width/24)):
        xpos = app.xpos + 24 * i - app.scrollX
        canvas.create_image(xpos, app.height/4, image = ImageTk.PhotoImage(app.tiles))
        canvas.create_image(xpos, app.height * 4/5, image = ImageTk.PhotoImage(app.tiles))
        canvas.create_image(app.width - 12 + xpos, app.height/4, image = ImageTk.PhotoImage(app.tiles))
        canvas.create_image(app.width - 12 + xpos, app.height * 4/5, image = ImageTk.PhotoImage(app.tiles))
    
    #player
    canvas.create_image(app.player.xpos - app.scrollX, app.player.ypos, image = ImageTk.PhotoImage(app.player.image))
    
    #obstacle
    for obstacle in app.obstacles:
        obstacle.drawObstacle(canvas, app.tiles, app.scrollX)
        
    #lives
    for j in range(len(app.player.lives)):
        if app.player.lives[j] == True:
            canvas.create_image(app.width * 5/6 + j*75, app.height/8, image = ImageTk.PhotoImage(app.fullheart))
        if app.player.lives[j] == False:
            canvas.create_image(app.width * 5/6 + j * 75, app.height/8, image = ImageTk.PhotoImage(app.emptyheart))

    #GAME OVER SEQUENCE
    if app.isDead == True and app.player.dyingFrame >= 10:
        canvas.create_text(app.width/2, app.height/2, text = "GAME OVER", font = "Arial 72 bold", fill = "white")
runApp(width = 1500, height = 532)