function Lsq = Lsquared(H, Y) % hypothesis vs actual

Lsq = sqrt(sum(sum((H - Y).^2)));
