from cmu_112_graphics import *

def appStarted(app):
    app.ogtile = app.loadImage('Images/tiles.png')
    app.tile = app.scaleImage(app.ogtile, 1/3)
    app.multiplier = 0 # 48
    app.position = app.width

def redrawAll(app, canvas):
    for i in range(int(app.width/24)):
        #upper
        canvas.create_image(24/2 + 24*i, app.height/4,
                            image=ImageTk.PhotoImage(app.tile))
        
        #lower
        canvas.create_image(24/2 + 24*i, 3 * app.height/4,
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