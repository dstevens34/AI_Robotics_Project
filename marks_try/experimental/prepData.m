function v = prepData(data, steps)

x = data(end-steps:end,1);
y = data(end-steps:end,2);

[xs, x_y] = featurize(x, steps);
[ys, y_y] = featurize(y, steps);

v = [xs(:,2:end), x_y, ys(:,2:end), y_y];
