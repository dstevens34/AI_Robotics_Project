function [test_score, cv_score] = test (steps)

% FIXME : I don't work with 3-5 steps, but should
% may be because I need to also create the file splits

load training_data.txt;

inlist = dir("splits/inputs/*");
outlist = dir("splits/actual/*");

for i=1:size(inlist)(1);
    eval(["load splits/inputs/", inlist(i).name]);
end;

for i=1:size(outlist)(1);
    eval(["load splits/actual/", outlist(i).name]);
end;

% build the KB
KB = buildKB (training_data, steps);

% disp("size of KB:");
% disp(size(KB));

test_scores = [];
cv_scores = [];

% using odd datasets for testing

% grab the odd numbered ins and outs
% for each name sans in/out component:

% where a is xaa01in, tell if the num is odd...
% mod(str2num(a(4:5)),2) != 0

% kludgy way of dealing with data/strings, but works
for i=1:size(inlist)(1);
  name = inlist(i).name(1:end-4); % remove .txt extension
  outf = strcat("X", name(5:end));
  % disp("predicting from:");
  % disp(name);
  predicted = predict60(KB, eval(name), steps);
  if mod(str2num(name(5:6)),2) != 0; % odd numbered datasets
     test_scores = [test_scores, Lsquared(predicted, eval(outf))];
  else
     cv_scores   = [cv_scores,   Lsquared(predicted, eval(outf))];
  end;
end;

test_score = mean(sort(test_scores)(1,2:end-1));
cv_score = mean(sort(cv_scores)(1,2:end-1));
