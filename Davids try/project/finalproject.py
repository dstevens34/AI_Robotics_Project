from PointHistory import PointHistory
from Functions import Functions
import sys

class finalproject:
    #opens the history and imports all points
    def __init__(self, FileName):

        try:
            #point history takes the file name and pulls in past history
            #returns list of points
            pointHistory = PointHistory("CombinedInputs.txt")
        except:
            #if the project can not find it in the main folder it will pull
            #from the project folder
            #returns list of points
            pointHistory = PointHistory("project/CombinedInputs.txt")
        #creates a function class
        func = Functions()
        #reads in the file that was passed and returns the points
        currentPoints = func.ReadInFile(FileName)
        file = open("prediction.txt",'w')

        index = 0
        #gets the last 2 points
        point1 = currentPoints[len(currentPoints)-2]
        point2 = currentPoints[len(currentPoints)-1]

        #gets next 60 points
        while(index < 60):
            #prediction history takes in the last 2 points and returns
            #possible next point
            predictPoint = pointHistory.nextPoint(point2, point1)
            #if it was not found, it returns the next possible point with the same slope
            if predictPoint == (-1,-1):
                x = point2[0]-point1[0]
                x = point2[0] + x
                y = point2[1]-point2[1]
                y = point2[1] + y
                predictPoint = (x,y)
            #creates output string
            output = str(predictPoint[0]) + "," + str(predictPoint[1]) + "\n"
            #writes out the output
            file.write(output)
            #updates the points
            point1 = point2
            point2 = predictPoint
            index += 1

        #closes the file
        file.close()

#main program
def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <testfile>" % sys.argv[0]
        sys.exit(1)

    finalproject(sys.argv[1])



if __name__ == "__main__":
    main()
