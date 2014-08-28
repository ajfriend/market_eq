%% Testing this waterfilling idea
rand('state',4)

n = 50;
y = rand(n,1); c = 0.3;

% Get solution
cvx_begin
    variable x(n)
    minimize(norm(x-y,2))
    subject to
        x>=0
        sum(x)==c
cvx_end

% Try waterfilling
delta = sum(y)-c;
x2 = y; k = n;
while (delta~=0)&&(k>1)
    ind = x2; ind(x2==0) = inf;
    x2 = x2 - min(min(ind),delta/k)*ones(n,1);
    x2(x2<0) = 0;
    k = k-1;
    delta = sum(x2)-c;
end
