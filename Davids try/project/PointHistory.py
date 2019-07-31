from Functions import Functions

class PointHistory:

    points = ()
    
    def __init__(self, FileName):
        func = Functions()
        self.points = func.ReadInFile(FileName)
        
    #takes in last 2 points and looks through history to see if the next point exist
    #
    def nextPoint(self, currentPoint, pointBefore):
        #this is the distance away the points can be. Will not go on forever
        shifting = [0, -1, 1, -2, 2]
        #loops through all the points to see if there is a match.
        for shiftx in shifting:
            for shifty in shifting:
                ShiftCurrent = (currentPoint[0] + shiftx, currentPoint[1]  + shifty)
                ShiftBefore = (pointBefore[0]  + shiftx, pointBefore[1]  + shifty)
        
                i = 1
                while i < len(self.points):            
                    if ShiftCurrent[0] == self.points[i][0] and ShiftCurrent[1] == self.points[i][1] and ShiftBefore[0] == self.points[i-1][0] and ShiftBefore[1] == self.points[i-1][1]:
                        if i+1 < len(self.points):
                            if self.points[i+1] != (-1,-1):
                                return (self.points[i+1][0] - shiftx, self.points[i+1][1] - shifty)
                    i += 1

        return (-1,-1)
