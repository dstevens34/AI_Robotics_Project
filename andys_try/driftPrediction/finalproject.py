"""
Reads in an input file and predicts the next 60 frames
"""

from math import atan2, sqrt, cos, sin
import os
import pandas as pd
import sys


def convert_line(line):
    x, y = line.split(',')
    return int(x.strip()), int(y.strip())


def get_angle(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_dist(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def get_drift(p1, p2, p3):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    xp = int(p2[0] + dx)
    yp = int(p2[1] + dy)
    drift = get_dist(p3, [xp, yp])
    x_drift = xp - p3[0]
    y_drift = yp - p3[1]

    return drift, x_drift, y_drift


def predict_parameters(training, loc):

    range = 5

    while True:

        mask = (training['x'] <= loc[0] + range) & \
               (training['x'] >= loc[0] - range) & \
               (training['y'] <= loc[1] + range) & \
               (training['y'] >= loc[1] - range)

        rows = training.loc[mask]

        if len(rows) > 0:

            angle = rows['angle'].mean()
            dist = rows['dist'].mean()
            drift_x = rows['x_drift'].mean()
            drift_y = rows['y_drift'].mean()

            return angle, dist, drift_x, drift_y

        range += 1

        if range > 100:
            # failed to find a match
            return 0, 0, 0, 0


def add_motion(loc, angle, dist, drift_x, drift_y):

    loc_p = loc[0] + (dist * cos(angle)) + drift_x, loc[1] + (dist * sin(angle)) + drift_y
    return loc_p


def predict_for(input_file):

    # get the input data
    data = [convert_line(line) for line in open(input_file, 'r').readlines()]

    # get the training data
    path = os.path.dirname(os.path.realpath(__file__))

    with open(path + "/training.csv", 'r') as csv:
        training = pd.read_csv(csv)

    # get the last three locations as a starting point
    p3 = data[-1]
    p2 = data[-2]
    p1 = data[-3]

    dist = get_dist(p3, p2)
    angle = get_angle(p3, p2)
    drift, drift_x, drift_y = get_drift(p1, p2, p3)

    preds = []

    # the first prediction is based off of the last point
    loc = add_motion(p3, angle, dist, drift_x, drift_y)

    preds.append(loc)

    for i in range(1, 60):

        # find the drift/angle for our location
        angle, dist, drift_x, drift_y = predict_parameters(training, loc)

        loc = add_motion(loc, angle, dist, drift_x, drift_y)

        preds.append(loc)


    return preds


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <testfile>" % sys.argv[0]
        sys.exit(1)

    print "Predicting input file %s" % sys.argv[1]
    predict_for(sys.argv[1])
