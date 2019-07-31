import operator

class Functions:
    #not used, this takes in 3 points and returns the a, b , c for a quad equation
    def QuadCreate(self, point1, point2, point3):
        x1 = point1[0]
        x2 = point2[0]
        x3 = point3[0]
        y1 = point1[1]
        y2 = point2[1]
        y3 = point3[1]
        a = ""
        b = ""
        c = ""
        x4 = ""
        x5 = ""
        x6 = ""
        x7 = ""
        y4 = ""
        y5 = ""

        y4 = y1-y2
        x4 = x1**2 - x2**2
        x5 = x1 - x2

        y5 = y1-y3
        x6 = x1**2 - x3**2
        x7 = x1 - x3

        tmpy4 = y4 * x7
        tmpx4 = x4 * x7
        tmpy5 = y5 * x5
        tmpx6 = x6 * x5
        if (tmpx4 - tmpx6) == 0:
            a = 1
        else:
            a = (tmpy4 - tmpy5)/(tmpx4 - tmpx6)

        if x7 == 0:
            b = 1
        else:
            b = (y5 - (x6*a))/x7

        c = y1 - (a*x1**2)- (b*x1)

        quadDic = {'a':a,'b':b,'c':c}
        return quadDic

    #reads in a file and returns points
    def ReadInFile(self, file_location):
        # file_location = r'C:\Users\Carrot\Documents\GitHub\CS8803\Resources\Inputs\test01.txt'

        with open(file_location , 'r') as content_file:
            content = content_file.read()

        content = content.split("\n")

        array = []

        for val in content:
            x = val.split(",")
            if x != ['']: # in case of empty line in test file
                array.append([int(x[0]),int(x[1])])
        return array

    #not used, calculates the rectangle of the area and adds in an additional
    #range. If the current_location is within that range returns true
    def WithinRangeSides(self, points, current_location, Rangex = 10, Rangey = 10):

        xMin = sorted(points)[0][0]
        xMax = sorted(points)[len(points)-1][0]
        points.sort(key=operator.itemgetter(1))
        yMin = points[0][1]
        yMax = points[len(points)-1][0]

        if xMin >= current_location - Rangex:
            return true
        if xMax <= current_location + Rangex:
            return true
        if yMin >= current_location[1]-Rangey:
            return true
        if yMax <= current_location[1]+Rangey:
            return true
        else:
            return false

    #not used, calculates the candle of the area and adds in an additional
    #range. If the current_location is within that range returns true
    def WithinRangeCandle(self, current_location, Range = 5):
        Radius = 5 + 34
        Candle_Center = (334, 178)

        if (current_location[0] - Candle_Center[0])**2 - (current_location[1] - Candle_Center[1])**2 <= Radius**2:
            return true
        else:
            return false
