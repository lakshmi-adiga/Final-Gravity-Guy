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
        self.xpos += dx*1.3
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
    
    def killYourself(self, animation, height):
        self.image = animation[0]
        if self.ypos <= height - 40:
            self.ypos += 10
        else:
            if self.dyingFrame < 10:
                    self.image = animation[self.dyingFrame//2]
                    self.dyingFrame += 1
            else:
                self.image = animation[5]
                
def isLegal(obstacles): #self, xpos, ypos, width, height
    if len(obstacles) == 1:
        return True
    else:
        for element in obstacles:
            for element1 in obstacles:
                if element != element1:
                    pass
                        
    
def placeObstacles(obstacles, level, screenstart, screenwidth):
    if level == 0:
        return obstacles
    else:
        ypos = random.randint(0, 1)
        if ypos == 0:
            ypos = 532 * 4/5 - 24 #isdown
        if ypos == 1:
            ypos = 532/4 + 24 #isup
            
        insert = Obstacle(random.randint(screenstart, screenwidth), ypos, random.randint(1, 4), random.randint(1, 8)) 
        obstacles.add(insert)
        
        if isLegal(obstacles):
            pass
        # for move in possibleMoves:
        #     if move is legal:
        #         solution = placeObstacle(obstacles, level-1)
        #         if solution != None:
        #             return solution
        #         *undo move*
        # return None
    
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
    
    def drawObstacle(self, canvas, image, scrollX):
        if self.isdown == True:
            for j in range(self.height):
                for i in range(self.width):
                    canvas.create_image(self.xpos + i*24 - scrollX, self.ypos - j*24, image=ImageTk.PhotoImage(image))
        if self.isup == True:
            for j in range(self.height):
                for i in range(self.width):
                    canvas.create_image(self.xpos + i*24 - scrollX, self.ypos + j*24, image = ImageTk.PhotoImage(image))
        
def appStarted(app):
    app.timerDelay = 1
    app.timerCounter = 0
    app.level = 1
    
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
    app.player = Player(app.width/2, app.height*4/5 - 40, 
                        app.charrunning, app.charjumping, 
                        app.upsidedownrunning)
    app.standing = True
    app.running = False
    app.jumping = False
    app.isAbove = False
    app.isBelow = True
    app.isDead = False
    
    #obstacle
    app.obstacles = set()
    app.obstacles.add(Obstacle(3 * app.width/4, app.height/4 + 24, 3, 8))
    app.obstacles.add(Obstacle(3*app.width/4 + 24 * 6, app.height * 4/5 - 24, 4, 3))
    
    #lives
    app.ogfullheart = app.loadImage("Images/fullheart.png")
    app.fullheart = app.scaleImage(app.ogfullheart, 1/4)
    app.ogemptyheart = app.loadImage("Images/emptyheart.png")
    app.emptyheart = app.scaleImage(app.ogemptyheart, 1/4)
    
def timerFired(app):
    app.timerCounter += 1

    #check if player has died
    if len(app.obstacles) != 0:
        for obstacle in app.obstacles:
            if app.player.died(obstacle):
                app.running = False
                app.standing = True
                app.isDead = True
    
    #background 
    if app.isDead == False:
        app.scrollX += 10
    if app.width/2 + app.posX1 - app.scrollX <= 0:
        app.posX1 += app.width * 2 
    if app.width/2 + app.posX2 - app.scrollX <= 0:
        app.posX2 += app.width * 2
    
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
    if app.standing == True and app.isDead == True:
        app.player.killYourself(app.dyinganimation, app.height)
    if app.player.image == app.dyinganimation[-1]:
        app.player.lives.pop(0)
        app.player.lives.append(False)

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
    # # GAME OVER SEQUENCE
    # if app.isDead == True and app.player.dyingFrame >= 10:
    #     canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    #     canvas.create_text(app.width/2, app.height/2, text = "GAME OVER", font = "Arial 72 bold", fill = "white")
    # else:
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
    
runApp(width = 1500, height = 532)