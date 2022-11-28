from cmu_112_graphics import *

def generateTerrain(terraingrid):
    #len(app.terraingrid) = rows
    #len(app.terraingrid[0]) = columns
    for i in range(len(terraingrid)):
        terraingrid[i][10][0] = True

def appStarted(app):
    app.scrollX = 0
    app.timerDelay = 1
    
    #terrain tiles
    app.ogtiles = app.loadImage("Images/tiles.png")
    app.tiles = app.scaleImage(app.ogtiles, 1/3)
    
    #grid
    app.terraingrid = []
    for k in range(app.width//24 + 1):
        a = []
        for l in range(app.height//24 + 1):
            a.append([False, (k*24) - 12, (l*24)-12])
        app.terraingrid.append(a)
        print(a)
        print("\n")
    
    for i in range(7, 20):
        app.terraingrid[i][len(app.terraingrid[0])//4][0] = True
        app.terraingrid[i][3 * len(app.terraingrid[0])//4][0] = True
        
def timerFired(app):
    app.scrollX += 1

def redrawAll(app, canvas):
    for row in app.terraingrid:
        for tile in row:
            if tile[0] == True:
                canvas.create_image(tile[1], tile[2], image=ImageTk.PhotoImage(app.tiles))
    
    canvas.create_image(app.width/2 - app.scrollX, app.height/2, image=ImageTk.PhotoImage(app.tiles))
runApp(width = 1488, height = 528)