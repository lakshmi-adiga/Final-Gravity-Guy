from cmu_112_graphics import *

def appStarted(app):
    app.tile = app.loadImage("Images/tiles.png")
    app.multiplier = 0 # 48
    app.position = app.width

def redrawAll(app, canvas):
    canvas.create_image(24/2 + 24, app.height/4,
                            image=ImageTk.PhotoImage(app.tile))
    canvas.create_image(24/2 + 24, 3 * app.height/4,
                            image=ImageTk.PhotoImage(app.tile))
        
    # for i in range(int(app.multiplier/2)):
    #     xpos1 = 22/2 + 22*i
    #     if xpos1 < 0:
    #         xpos1 += app.width
    #     canvas.create_image(xpos1, app.height/4,
    #                         image=ImageTk.PhotoImage(app.tile))
    #     canvas.create_image(xpos1, 3 * app.height/4,
    #                         image=ImageTk.PhotoImage(app.tile))

runApp(width = 1500, height = 532)