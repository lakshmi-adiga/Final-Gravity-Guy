from cmu_112_graphics import *
from classes import *

def appStarted(app):
    app.timerDelay = 1
    
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
    app.chars = []

    for i in range(6):
        char = app.charstrip.crop((i*55, 0, 55*(i+1), 65))
        app.chars.append(char)
    
    app.charcopy = copy.copy(app.chars)
    
    for i in range(6):
        app.chars.append(app.charcopy[5-i])
        
    app.charCounter = 0
    app.isRunning = False
    
def timerFired(app):
    #background 
    app.scrollX += 10
    if app.width/2 + app.posX1 - app.scrollX <= 0:
        app.posX1 += app.width * 2 
    if app.width/2 + app.posX2 - app.scrollX <= 0:
        app.posX2 += app.width * 2
    
    #terrain
    if app.xpos + 24 * (int(app.width/24)-1) - app.scrollX <= 0:
        app.xpos += app.width
    
    
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
     
runApp(width = 1500, height = 532)