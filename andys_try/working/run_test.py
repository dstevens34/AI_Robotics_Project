
import KNNLearner as knn
from math import atan2, sqrt
from matplotlib import  pyplot as plt
import numpy as np
from math import *


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


def run_test(file_num):

    leaner = knn.KNNLearner(verbose=False)

    input_file = 'Inputs/test%02d.txt' % file_num
    data = [convert_line(line) for line in open(input_file, 'r').readlines()]

    num_test = 120

    x = data[0][0]
    y = data[0][1]
    dist = get_dist(data[0], data[1])
    angle = get_angle(data[0], data[1])

    k = 7
    print "starting loc:", x, ",", y
    preds = []

    for i in range(num_test):

        print "Input:", x, y
        x, y, angle, dist = leaner.predict(k, x, y, angle, dist)

        print "X:", x, "Y:", y, "Angle:", angle, "dist:", dist
        preds.append((x,y))

    acts = np.array(data[0:num_test])
    targets = np.array(preds)

    plt.scatter(acts[:, 0], acts[:, 1], color='green')
    plt.scatter(targets[:, 0], targets[:, 1], color='red')
    plt.show()
    #plt.savefig("predict.png")

if __name__ == "__main__":
    run_test(1)