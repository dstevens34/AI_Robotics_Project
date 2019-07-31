function H = predict60(KB, data, steps) % where data is 2 col x,y data from test file

% convert test data to vec for comparing to vecs in KB
% just use the last <steps> number of points for test vector
tv = [data(end-steps+1:end,1)', data(end-steps+1:end,2)'];

% compare only to step-num in KB, leaving other 60 steps for output

x_steps_KB = KB(:,1:steps);
y_steps_KB = KB(:,steps+60+1:steps+60+steps);

% disp("x steps KB:");
% disp("y steps KB:");
% size(y_steps_KB)

tmat = repmat(tv, size(KB)(1), 1);
% disp("tmat size:");
% size(tmat)


diffs = sum(([x_steps_KB y_steps_KB] - tmat).^2, 2);

closest = min(diffs);
idx = find(diffs == closest)(1,:); % later, use the multiple mins when they occur
% disp("size of idx:");
% size(idx)

p = KB(idx,:);
% disp("size of p:");
% size(p)
x_ans = p(steps+1:steps+60);
y_ans = p(steps+60+steps+1:end);

% disp("Y ans size:");
% disp(size(y_ans));
% disp("X ans size:");
% disp(size(x_ans));

% return x,y list in 2 column matrix
H = [x_ans' y_ans'];
