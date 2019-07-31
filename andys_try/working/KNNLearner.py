
import numpy as np
from scipy.spatial import distance
import pandas as pd
import random
import os

class KNNLearner(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

        path = os.path.dirname(os.path.realpath(__file__))

        with open(path + "/training.csv", 'r') as csv:
            self.training = pd.read_csv(csv)

        with open(path + "/training_normed.csv", 'r') as csv:
            self.training_normed = pd.read_csv(csv)

        with open(path + "/means.csv", 'r') as csv:
            mean = pd.read_csv(csv)
            self.mean_x = mean.iloc[0][1]
            self.mean_y = mean.iloc[1][1]
            self.mean_angle = mean.iloc[2][1]
            self.mean_dist = mean.iloc[3][1]

        with open(path + "/stds.csv", 'r') as csv:
            std = pd.read_csv(csv)
            self.std_x = std.iloc[0][1]
            self.std_y = std.iloc[1][1]
            self.std_angle = std.iloc[2][1]
            self.std_dist = std.iloc[3][1]

    def predict(self, k, x, y, angle, dist):

        if self.verbose:
            print
            print "Predicting for x:", x, "y:", y, "angle:", angle, "dist:", dist

        x_init = x
        y_init = y
        angle_init = angle
        dist_init = dist

        # normalize the input
        x = (x - self.mean_x) / self.std_x
        y = (y - self.mean_y) / self.std_y
        angle = (angle - self.mean_angle) / self.std_angle
        dist = (dist - self.mean_dist) / self.std_dist

        point = np.array([(x, y, angle)])
        cols = ['x', 'y', 'angle']

        values = self.training_normed[cols].values

        # find the nearest neighbors
        distResult = distance.cdist(point, values, 'euclidean')

        sortdex = np.argsort(distResult, axis=1)

        mindex = sortdex[:,0:k][0]

        row_distances = 1 / distResult[0][mindex]
        dist_sum = sum(row_distances)
        weights = row_distances / dist_sum

        if self.verbose:
            print "mindex:", mindex
            print "row_distances:", row_distances
            print "Weights:", weights

        data_rows = self.training.iloc[mindex]

        x_p = 0.
        y_p = 0.
        angle_p = 0.
        dist_p = 0.

        # calculate the weighted result
        for i in range(k):

            weight = weights[i]

            if self.verbose:
                print
                print "weight:", weight, "dest_x:", data_rows.iloc[i]['dest_x'], \
                    "dest_y:", data_rows.iloc[i]['dest_y'], "angle:", data_rows.iloc[i]['angle'], \
                    "dist:", data_rows.iloc[i]['dist']

                print
                print "Data row", i
                print data_rows.iloc[i]
                print

            x_p += data_rows.iloc[i]['dest_x'] * weight
            y_p += data_rows.iloc[i]['dest_y'] * weight
            angle_p += data_rows.iloc[i]['angle'] * weight
            dist_p += data_rows.iloc[i]['dist'] * weight

        x_p = int(x_p)
        y_p = int(y_p)

        # add some noise to the output
        x_p = random.gauss(x_p, 0.01 * x_p)
        y_p = random.gauss(y_p, 0.01 * y_p)
        angle_p = random.gauss(angle_p, 0.05 * angle_p)
        dist_p = random.gauss(dist_p, 0.05 * dist_p)

        if self.verbose:
            print
            print "result: x:", x_p, "y:", y_p, "angle:", angle_p, "dist:", dist_p

        return x_p, y_p, angle_p, dist_p

