from cmu_112_graphics import *
import random

#varmarker to save to github
GithubSave = True

def isLegal(obstacles, randompos, randomheight): # randompos = 
    if (randompos, randomheight) in obstacles:
        return False
    

#obstacle backtracking
def placeObstacle(obstacles, maybex, maybey, level):
    if level == 0:
        return obstacles
    else:
        posy = maybey[random.randint(0, 1)]
        if posy == 1:
            posy = len(maybey) - 1
            
        randompos = (maybex[random.randint(0, len(maybex))],
                     posy)
        randomheight = random.randint(0, len(maybey) - 1)
        if isLegal(obstacles, randompos, randomheight):
            obstacles.append((randompos, randomheight))
            solution = placeObstacle(obstacles, maybex, maybey, level - 1)
            if solution != None:
                return solution
            else:
                obstacles.remove((randompos, randomheight))
        return None
            
class Obstacle():
    def __init__(self, xpos, ypos, width, height):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        
class Player():
    def __init__(self, xpos, ypos, charrunning, charjumping, upsidedownrun):
        self.xpos = xpos
        self.ypos = ypos
        self.charrunning = charrunning
        self.charjumping = charjumping
        self.upsidedownrun = upsidedownrun
        self.image = self.charrunning[0] 
    
    def isStanding(self):
        self.image = self.charrunning[0]
    
    def isRunning(self, dx, frame):
        charsList = copy.copy(self.charrunning)
        charsList.pop(0)
        self.xpos += dx
        self.image = charsList[frame]
    
    def upsideDownRunning(self, dx, frame):
        charsList = copy.copy(self.upsidedownrun)
        charsList.pop(0)
        self.xpos += dx
        self.image = charsList[frame]
    
    def isJumping(self, dx, frame):
        self.xpos += dx*1.3
        if self.ypos >= 187:
            self.ypos -= 35
            self.image = self.charjumping[frame]
            if self.image == self.charjumping[-2]:
                self.image = self.charjumping[-1]
    
    def isDownJump(self, dx, frame):
        self.xpos += dx*1.3
        if self.ypos < 385:
            self.ypos += 35
            self.image = self.charjumping[frame]

def appStarted(app):
    app.timerDelay = 1
    app.timerCounter = 0
    app.level = 2
    
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
      
    #player
    app.player = Player(app.width/2, app.height*4/5 - 40, app.charrunning, app.charjumping, app.upsidedownrunning)
    app.standing = True
    app.running = False
    app.jumping = False
    app.isAbove = False
    app.isBelow = True
    
    #obstacle
    app.obstaclegridx = []
    i = 0
    while i < app.width:
        app.obstaclegridx.append(i)
        i += 24
    
    app.obstaclegridy = []
    j = app.height/4 + 12
    while j < app.height * 4/5:
        app.obstaclegridy.append(j)
        j += 24
        
    app.obstacles = []
    app.finalobstacles = placeObstacle(app.obstacles, app.obstaclegridx, app.obstaclegridy, app.level)
    print(app.finalobstacles)
    
def timerFired(app):
    app.timerCounter += 1
    
    #background 
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

def keyPressed(app, event):
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
     
    #obstaclegrid
    for coordinatex in range(len(app.obstaclegridx) - 1):
        for coordinatey in range(len(app.obstaclegridy) - 1):
            if app.obstaclegridx[coordinatex + 1] - app.scrollX <= 0:
                canvas.create_rectangle(app.obstaclegridx[coordinatex] + app.width,
                                        app.obstaclegridy[coordinatey],
                                        app.obstaclegridx[coordinatex + 1] + app.width ,
                                        app.obstaclegridy[coordinatey + 1])
            canvas.create_rectangle(app.obstaclegridx[coordinatex], app.obstaclegridy[coordinatey],
                                    app.obstaclegridx[coordinatex + 1], app.obstaclegridy[coordinatey + 1])

runApp(width = 1500, height = 532)