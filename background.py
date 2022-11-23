from cmu_112_graphics import *

def appStarted(app):
    app.bg = app.loadImage('Images/bg1.png')
    app.bg2 = app.loadImage('Images/bg1.png')
    app.scrollX = 0
    app.pos1 = app.width/2
    
def timerFired(app):
    app.scrollX += 100
    if app.scrollX % app.width == 0:
        app.pos1 += app.width

def redrawAll(app, canvas):
    canvas.create_image(app.pos1 - app.scrollX, app.height/2,
                        image=ImageTk.PhotoImage(app.bg))
    canvas.create_image(app.pos1 + app.width - app.scrollX, app.height/2, image=ImageTk.PhotoImage(app.bg))      
    
runApp(width = 1488, height = 532)