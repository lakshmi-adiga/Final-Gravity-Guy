from cmu_112_graphics import *

class Player():
    def __init__(self, xpos, ypos, chars):
        self.xpos = xpos
        self.ypos = ypos
        self.chars = chars
        self.image = self.chars[0] 
    
    def isStanding(self):
        self.image = self.chars[0]
    
    def isRunning(self, dx, frame):
        charsList = copy.copy(self.chars)
        charsList.pop(0)
        self.xpos += dx
        self.image = charsList[frame]
    
    def isJumping(self, direction, dx):
        pass

def appStarted(app):
    app.timerDelay = 1
    app.timerCounter = 0
    #background
    app.bg = app.loadImage("Images/bg1.png")
    app.posX1 = app.width/2
    app.posX2 = app.width/2 * 3
    app.scrollX = 0
    
    #terrain
    app.ogtiles = app.loadImage("Images/tiles.png")
    app.tiles = app.scaleImage(app.ogtiles, 1/3)
    app.xpos = 12
    
    #creation of the app.chars list
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
    
    #player
    app.player = Player(app.width/8, app.height*4/5 - 40, app.charrunning)
    app.running = False
    app.charCounter = 0   
    
    
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
    if app.running == True:
        app.player.isRunning(10.5, app.timerCounter % 6)
    if app.running == False:
        app.player.isStanding()
    
def keyPressed(app, event):
    if (event.key == "Right"):
        app.running = True
    if (event.key == "Down"):
        app.running = False
    
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
     
runApp(width = 1500, height = 532)