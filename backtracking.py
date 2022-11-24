
#TODO: Backtracking for obstacle viability
 
def isFull():
    pass
def isEmpty():
    pass
def isLegal():
    pass

def placeObstacleHelper(): #state
    if isFull(): #state
        return () #state
    else:
        possiblePositions = () #insert all possible positions here
        for position in possiblePositions:
            if isLegal():
                solution = placeObstacleHelper() #new state
                if solution != None:
                    return solution
                #else:
                    #undo moves you did to make it a new state
        return None
    
def placeObstacle(): #state
    if isEmpty(): #state (just check if the list of obstacles is empty)
        return True
    else:
        return placeObstacleHelper()
        