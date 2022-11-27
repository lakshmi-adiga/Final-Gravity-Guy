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
    
# #make a player class to be integrated into the rest of the code

# def appStarted(app):
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