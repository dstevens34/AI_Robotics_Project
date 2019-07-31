
"""
record 'drift' of the current heading
.i.e. if going straight, it would go a -> b, but instead it went a -> (b - c)
so 'c' gives us drift off of the straight line.

to predict next spot, move in straight line and subtract the drift
"""

#candle: 335, 180 (center), radius 30


from math import atan2, degrees, sqrt
import pandas as pd
import hexbug_visualize.visualizer as viz
import KNNLearner as knn


def get_angle(p1, p2):
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def get_dist(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def convert_line(line):
    x, y = line.split(',')
    return int(x.strip()), int(y.strip())

def process_training_data():
    """
    Process the raw training_data to calculate our additional data fields
    and write the dataframe to data/%d.txt
    """

    input = "training_data.txt"
    output = "training_normed.csv"


    print "Processing input file", input

    data = [convert_line(line) for line in open(input, 'r').readlines()]

    df = pd.DataFrame(data, columns=['x','y'])
    df["angle"] = 0.0
    df["dist"] = 0.0
    #df["drift"] = 0.0
    #df['xp'] = 0
    #df['yp'] = 0
    #df['x_drift'] = 0
    #df['y_drift'] = 0
    df['dest_x'] = 0
    df['dest_y'] = 0

    for i in range(1, len(df)):
        p1 = [df.loc[i-1,'x'], df.loc[i-1,'y']]
        p2 = [df.loc[i,'x'], df.loc[i,'y']]
        df.loc[i,'angle'] = get_angle(p1, p2)
        df.loc[i,'dist'] = get_dist(p1, p2)

        """

        if i == 1:
            continue  # need at least three points to calculate drift

        p0 = [df.loc[i-2,'x'], df.loc[i-2,'y']]

        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        xp = int(p1[0] + dx)
        yp = int(p1[1] + dy)
        x_drift = xp - p2[0]
        y_drift = yp - p2[1]

        df.loc[i, ('drift', 'xp', 'yp', 'x_drift', 'y_drift')] = (get_dist(p2, [xp, yp]), xp, yp, x_drift, y_drift )

        """

        if i < len(df) - 1:
            df.loc[i, ('dest_x', 'dest_y')] = (int(df.loc[i + 1]['x']), int(df.loc[i + 1]['y']))

        if i % 100 == 0:
            print i


    #write the un-normalized data
    df.to_csv("training.csv")

    cols = ['x', 'y', 'angle', 'dist']

    print df.head()

    means = df[cols].mean()
    stds = df[cols].std()

    df[cols] = (df[cols] - df[cols].mean()) / df[cols].std()

    print "after:"
    print df.head()

    print "means"
    print means

    print "stds"
    print stds

    print "Writing output to file", output
    df[cols].to_csv(output)
    means.to_csv("means.csv")
    stds.to_csv("stds.csv")

    # end process_test_data


def load_test_data():
    """
    load the pre-processed data
    """

    file_num = 1
    df = pd.read_csv('data/data%02d.txt' % file_num, index_col=0)
    return df


if __name__ == "__main__":

    #process_training_data()
    #normalize_training_data()
    #df = load_test_data()

    #print df

    learner = knn.KNNLearner()


    """
    ,x,y,angle,dist,drift,xp,yp,x_drift,y_drift,dest_x,dest_y
    2,278,64,0.343023940421,14.8660687473,7.21110255093,272,60,-6.0,-4.0,282,60
    3,282,60,-0.785398163397,5.65685424949,13.4536240471,292,69,10.0,9.0,296,67
    4,296,67,0.463647609001,15.6524758425,14.8660687473,286,56,-10.0,-11.0,306,59
    5,306,59,-0.674740942224,12.8062484749,15.5241746963,310,74,4.0,15.0,306,62
    6,306,62,1.57079632679,3.0,14.8660687473,316,51,10.0,-11.0,315,61
    7,315,61,-0.110657221174,9.05538513814,9.8488578018,306,65,-9.0,4.0,321,64
    """

    result = learner.predict(3, 278, 64, 0.3430239, 14.866068)

    print "Dest X:", result[0]
    print "Dest Y:", result[1]
    print "Angle :", result[2]
    print "Dist  :", result[3]


    """
    truth_set = df.ix[2:200,('x', 'y')]
    truth = [tuple(x) for x in truth_set.values]

    pred_set = df.ix[2:200,('xp', 'yp')]
    prediction = [tuple(x) for x in pred_set.values]

    blueColor = (255,150,50)
    redColor = (150,150,255)
    viz.setupColors(blueColor, redColor)

    viz.drawComparePositions(truth, prediction, 50., 1920, 1080, "predicted_path.jpg")
    """

    #print df

    #df['drift'].plot()

    """
    todo: add the resulting position (next time step) as features to each row
    then use a weighted KNN to find position of an input
    """


    #plt.show()

    #plt.scatter(df.x, df.y)

    #plt.show()


