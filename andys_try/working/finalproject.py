
import sys
import KNNLearner as knn
from math import atan2, sqrt


def convert_line(line):
    x, y = line.split(',')
    return int(x.strip()), int(y.strip())


def get_angle(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_dist(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def predict_for(input_file, num_to_predict=60):

    leaner = knn.KNNLearner(verbose=False)

    data = [convert_line(line) for line in open(input_file, 'r').readlines()]

    x = data[-1][0]
    y = data[-1][1]
    dist = get_dist(data[-2], data[-1])
    angle = get_angle(data[-2], data[-1])

    k = 5
    #print "starting loc:", x, ",", y
    preds = []

    for i in range(num_to_predict):
        #print "Input:", x, y
        x, y, angle, dist = leaner.predict(k, x, y, angle, dist)

        #print "X:", x, "Y:", y, "Angle:", angle, "dist:", dist
        preds.append((x, y))

    with open("prediction.txt", "w") as f:

        for i in range(len(preds)):
            f.write(str(int(preds[i][0])) + "," + str(int(preds[i][1])) + "\n")

        f.close()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <testfile>" % sys.argv[0]
        sys.exit(1)

    print "Predicting input file %s" % sys.argv[1]
    predict_for(sys.argv[1])