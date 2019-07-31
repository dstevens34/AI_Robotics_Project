#!/usr/bin/env python

# 1NN approach to solving hexbug prediction problem.
# Mark Whelan, 4/16/16


from numpy import *
from pprint import *
import pickle
import sys

seqlen=19 # number of points used in prediction
KB_pkl = "KB" + str(seqlen) + ".pkl"

def loadKBcsv(filename):
    return matrix(loadtxt(open(filename,"rb"),delimiter=",",skiprows=0))


# loading with pickle is much faster than reading csv (when tested)
def loadKBpkl(filename):
    f = open(filename, 'rb')
    KB = pickle.load(f)
    f.close()
    return KB


def predict60(KB, tvec, seqlen):
    x_steps_KB = KB[:, 0:seqlen]
    y_steps_KB = KB[:, seqlen+60:seqlen+60+seqlen]

    tmat = tile(tvec, (shape(KB)[0], 1))

    diffs = sum(square(hstack((x_steps_KB, y_steps_KB)) - tmat), axis=1)

    closest = min(diffs);
    idx = where(diffs == closest)
    p = KB[idx,:][0]

    x_ans = p[0][:, seqlen:seqlen+60]
    y_ans = p[0][:, seqlen+60+seqlen:]

    return hstack((transpose(x_ans), transpose(y_ans)))


def write_prediction_file(prediction, filename):
    f = open(filename, "w")
    for i in range(len(prediction)):
        f.write(str(int(prediction[i,0])) + "," + str(int(prediction[i,1])) + "\n")
    f.close()


# borrowed from grading.py
def convert_line(line):
    x, y = line.split(',')
    return int(x.strip()), int(y.strip())


# % convert test data to vec for comparing to vecs in KB
# % just use the last <steps> number of points for test vector
def load_test_vector(testfile, seqlen):
    test = []
    test.append([convert_line(line) for line in open(testfile, 'r').readlines()])
    testseq = test[0][len(test)-seqlen-1:]
    return hstack((transpose(matrix(testseq))[0], transpose(matrix(testseq))[1]))

def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <testfile>" % sys.argv[0]
        sys.exit(1)

    testfile = sys.argv[1]

    try:
        KB = loadKBpkl(KB_pkl)
    except:
        KB = loadKBpkl("project/" + KB_pkl)

    tvec = load_test_vector(testfile, seqlen)
    prediction = predict60(KB, tvec, seqlen)
    write_prediction_file(prediction, "prediction.txt")


if __name__ == "__main__":
    main()
