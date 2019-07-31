"""
This script pre-processes the training data to calculate:

 - angle: current heading angle
 - distance: distance traveled since last frame
 - predicted_x: predicted x coordinate based on previous 2 locations
 - predicted_y: predicted y coordinate based on previous 2 locations
 - drift_x: distance between x and predicted_x
 - drift_y: distance between y and predicted_y
 - dest_x: x coordinate of next frame
 - dest_y: y coordinate of next frame

 results are written to training.csv

 dataframe is then normalized to have a mean of 1 and std of 1

 normalized data is written to training_normed.csv
 stds are written to stds.csv
 means are written to means.csv

"""

from math import atan2, sqrt
import pandas as pd


def get_angle(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_dist(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def convert_line(line):
    x, y = line.split(',')
    return int(x.strip()), int(y.strip())


def process_training_data():

    input = "training_data.txt"
    output = "training.csv"
    output_normalized = "training_normed.csv"

    data = [convert_line(line) for line in open(input, 'r').readlines()]

    df = pd.DataFrame(data, columns=['x', 'y'])
    df["angle"] = 0.0
    df["dist"] = 0.0
    df['dest_x'] = 0
    df['dest_y'] = 0
    df['drift'] = 0
    df['xp'] = 0
    df['yp'] = 0
    df['x_drift'] = 0
    df['y_drift'] = 0

    for i in range(1, len(df)):
        p1 = [df.loc[i-1,'x'], df.loc[i-1,'y']]
        p2 = [df.loc[i,'x'], df.loc[i,'y']]
        df.loc[i,'angle'] = get_angle(p1, p2)
        df.loc[i,'dist'] = get_dist(p1, p2)

        if i == 1:
            continue  # need at least three points to calculate drift

        p0 = [df.loc[i-2,'x'], df.loc[i-2,'y']]

        # calculate drift
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        xp = int(p1[0] + dx)
        yp = int(p1[1] + dy)
        x_drift = xp - p2[0]
        y_drift = yp - p2[1]

        df.loc[i, ('drift', 'xp', 'yp', 'x_drift', 'y_drift')] = (get_dist(p2, [xp, yp]), xp, yp, x_drift, y_drift )

        if i < len(df) - 1:
            df.loc[i, ('dest_x', 'dest_y')] = (int(df.loc[i + 1]['x']), int(df.loc[i + 1]['y']))

        if i % 100 == 0:
            print i

    # write the un-normalized data
    df.to_csv(output)

    # normalize the data
    cols = ['x', 'y', 'angle', 'dist']

    means = df[cols].mean()
    stds = df[cols].std()

    # write the normalized data
    df[cols] = (df[cols] - df[cols].mean()) / df[cols].std()
    df[cols].to_csv(output_normalized)
    means.to_csv("means.csv")
    stds.to_csv("stds.csv")

    # end process_test_data


if __name__ == "__main__":
    process_training_data()