function y = predict(x)
  y = interp1(x(:,1), x(:,2), linspace(min(x(:,1)), max(x(:,1)), 100), 'spline');
end
