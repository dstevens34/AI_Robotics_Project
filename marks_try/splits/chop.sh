#!/usr/bin/env bash

# 3/12/16, mw
#
# This script operates within a directory containing the 10 testXX.txt files.
#
# It takes a number N as its argument. N needs to be evenly divisible into 1800.
# Each test file is first split into files N lines long. Then each of these files is
# split into two files, the first containing N-60 lines, to be used as input for testing,
# and the second containing the last 60 lines, to be used to compare test output to
# actual values.
#
# This lets us create many more test cases than just one for each test file, and this
# should help us prevent (over|under)fitting.
#
# Example use:
#
# Split each test files into muliple parts, 150 lines each. (1800/150 = 12 files for each
# test file, so we'll generate 120 test cases instead of just 10. Use half of these for cross
# validation.)
#
# $ ./chop.sh 150
#
# The inputs directory will contain 120 files each 90 lines long, in a "inputs"
# directory, and 120 more files each 60 lines long, in an "actual" directory.
#
# We can then run our predictive algorithms on 120 cases for this example. The file names
# correspond across the directories for each test case.

if [[ $# != 1 ]]; then
    echo "Usage: $0 <number of lines per file>"
    exit 1
fi

NUMLINES=$1
NUMFILESEACH=$(expr 1800 / $NUMLINES)
NUMFILESTOTAL=$(expr 10 \* $NUMFILESEACH)

echo "Creating $NUMFILESTOTAL test cases..."

for i in `seq -w 1 10`;do
    echo "Splitting test${i}.txt..."
    split -l $NUMLINES "test${i}.txt"
    for j in x??;do
        mv $j "${j}${i}"
    done
done

# rename to testXX
mkdir -p tmp
N=1
for i in x*;do
    NAME=$(seq -f "test%02g.txt" $N $N)
    mv $i tmp/$NAME
    N=$(expr $N + 1)
done

echo "Splitting new files into test input and actual output folders"

mkdir -p inputs
mkdir -p actual

NUM_XLINES=$(expr $NUMLINES - 60)

cd tmp
for i in *; do
    # echo "Processing $i"
    NAME=`echo $i|sed "s/test//"`
    tail -n 60 $i > ../actual/$NAME
    head -n $NUM_XLINES $i > ../inputs/"${i}"
done

cd ..
rm -rf tmp
