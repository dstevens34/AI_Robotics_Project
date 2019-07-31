#!/usr/bin/env python

from numpy import *
import pickle
import sys

if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: %s <csv file to convert to pkl>" % sys.argv[0]
    sys.exit(1)

filename = sys.argv[1]

def loadKB(filename):
    return matrix(loadtxt(open(filename, 'rb'), delimiter=",", skiprows=0))

def picklize(obj, filename):
    output = open(filename, 'wb')
    pickle.dump(obj, output)
    output.close()

KB = loadKB(filename)
picklize(KB, "KB20.pkl")
