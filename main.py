from cmu_112_graphics import *

def appStarted(app):
    app.timerDelay = 10
    
    #background
    app.bg = app.loadImage('bg1.png')
    app.bg2 = app.loadImage('bg1.png')
    app.scrollX = 0
    app.pos1 = app.width/2
    
    #tiles
    app.ogtile = app.loadImage('tiles.png')
    app.tile = app.scaleImage(app.ogtile, 1/3)
    app.multiplier = 0 # 48
    app.position = app.width

def timerFired(app):
    #background
    app.scrollX += 10
    if app.scrollX % app.width == 0:
        app.pos1 += app.width

def redrawAll(app, canvas):
    #background
    canvas.create_image(app.pos1 - app.scrollX, app.height/2,
                        image=ImageTk.PhotoImage(app.bg))
    canvas.create_image(app.pos1 + app.width - app.scrollX, app.height/2, 
                        image=ImageTk.PhotoImage(app.bg))
    #tiles
    for i in range(int(app.width/24)):
        #upper
        canvas.create_image(24/2 + 24*i - app.scrollX, app.height/4,
                            image=ImageTk.PhotoImage(app.tile))
        
        #lower
        canvas.create_image(24/2 + 24*i - app.scrollX, 3 * app.height/4,
                            image=ImageTk.PhotoImage(app.tile))
        
runApp(width = 1500, height = 532)