function [test_scores, cv_scores] = run ()

% run tests for steps of 3 to N
% run cross validation for same steps

% get number of steps for the 3 most optimum tests, same for cv

test_scores = [];
cv_scores = []
for i=2:140
    [t,cv] = test(i);
    test_scores = [test_scores; t];
    cv_scores = [cv_scores; cv];
end
