from cmu_112_graphics import *

def appStarted(app):
    app.bg = app.loadImage('bg.png')

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.bg))
    
runApp(width = 1504, height = 532)