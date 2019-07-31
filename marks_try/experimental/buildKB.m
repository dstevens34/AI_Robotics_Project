function KB = buildKB(M, steps) % 2nd param takes num steps to use for prediction

x = M(:,1);
y = M(:,2);
n = steps + 60;
m = size(M)(1) - n + 1

KB = []
for i=1:m
        next = shift(M, -(i-1))(1:n,:);
        KB= [KB; [next(:,1)', next(:,2)']];
end
