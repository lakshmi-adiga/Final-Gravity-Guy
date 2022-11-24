from cmu_112_graphics import *

# #make a player class to be integrated into the rest of the code

# def appStarted(app):
#     app.timerDelay = 50
    
#     #background
#     app.bg = app.loadImage("Images/bg1.png")
#     app.posX1 = app.width/2
#     app.posX2 = app.width/2 * 3
#     app.scrollX = 0
    
#     #terrain
#     app.ogtiles = app.loadImage("Images/tiles.png")
#     app.tiles = app.scaleImage(app.ogtiles, 1/3)
#     app.xpos = 12
    
#     #character running animation
#     app.ogcharacterstrip = app.loadImage("Images/running.png")
#     app.characterstrip = app.scaleImage(app.ogcharacterstrip, 1/2) #52
#     app.characters = []

#     for i in range(6):
#         character = app.characterstrip.crop((i*55, 0, 55*(i+1), 65))
#         app.characters.append(character)
    
#     app.charcopy = copy.copy(app.characters)
    
#     for i in range(6):
#         app.characters.append(app.charcopy[5-i])
        
#     app.charCounter = 0
    
#     #changing in between running and standing
#     app.isRunning = False
    
#     app.ogstanding = app.loadImage("Images/standing.png")
#     app.standing = app.scaleImage(app.ogstanding, 1/2)

# def timerFired(app):
#     app.charCounter += 1
#     app.charCounter %= len(app.characters)

# def keyPressed(app, event):
#     if event.key == "Right":
#         app.isRunning = True #the bug is that if you keep clicking right it will keep redoing the thing 

# def redrawAll(app, canvas):
#     #character
#     #len(app.characters) = 6, mid is 33
#     if app.isRunning == True:
#         canvas.create_image(app.width/2 - app.scrollX, app.height * 4/5 - 43, image=ImageTk.PhotoImage(app.characters[app.charCounter]))
#     if app.isRunning == False:
#         canvas.create_image(app.width/2 - app.scrollX, app.height * 4/5 - 43, image=ImageTk.PhotoImage(app.standing))

# runApp(width = 1500, height = 532)