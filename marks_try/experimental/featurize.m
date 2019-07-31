function [X,y] = featurize(v, n, orders=[1]) % n = num previous time steps

% orders = polynomial orders to add other than 1

  m = size(v,1) - n; % number of training examples
  orders_len = size(orders)(2)

  y = shift(v,-n)(1:end-n,:);

  X1 = [] % X1 <= order 1 polynomial
  for i=1:n,
          X1 = [X1, shift(v,-(i-1))(1:m)];
  end;

  X = []
  for i=1:orders_len, % (columns only)
          X = [X, X1 .^ orders(1,i)];
  end;
