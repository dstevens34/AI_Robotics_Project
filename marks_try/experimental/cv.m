function score = cv (steps)

load training_data.txt
load 1740/test01.txt
load 1740/test02.txt
load 1740/test03.txt
load 1740/test04.txt
load 1740/test05.txt
load 1740/test06.txt
load 1740/test07.txt
load 1740/test08.txt
load 1740/test09.txt
load 1740/test10.txt
load 60/y01.txt
load 60/y02.txt
load 60/y03.txt
load 60/y04.txt
load 60/y05.txt
load 60/y06.txt
load 60/y07.txt
load 60/y08.txt
load 60/y09.txt
load 60/y10.txt

% build the KB
KB = buildKB (training_data, steps);

scores = [];

% using even datasets for cross-validation
%scores = [scores, Lsquared(predict60(KB, test01, steps), y01)];
scores = [scores, Lsquared(predict60(KB, test02, steps), y02)];
%scores = [scores, Lsquared(predict60(KB, test03, steps), y03)];
scores = [scores, Lsquared(predict60(KB, test04, steps), y04)];
%scores = [scores, Lsquared(predict60(KB, test05, steps), y05)];
scores = [scores, Lsquared(predict60(KB, test06, steps), y06)];
%scores = [scores, Lsquared(predict60(KB, test07, steps), y07)];
scores = [scores, Lsquared(predict60(KB, test08, steps), y08)];
%scores = [scores, Lsquared(predict60(KB, test09, steps), y09)];
scores = [scores, Lsquared(predict60(KB, test10, steps), y10)];

score = mean(sort(scores)(1,2:end-1));
