from cmu_112_graphics import *

def appStarted(app):
    terraingrid = []
    for k in range(app.width//24 + 1):
        for l in range(app.height//24):
            pass
def redrawAll(app, canvas):
    for k in range(app.width//24 + 1):
        for l in range(app.height//24 + 1):
            canvas.create_rectangle(k * 24, l * 24, (k+1) * 24, (l+1) * 24)
            canvas.create_text((k*24) - 12, (l*24) - 12, text = "True")
    
runApp(width = 1488, height = 528)