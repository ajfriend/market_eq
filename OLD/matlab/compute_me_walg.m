function [X,p] = compute_me_walg(A,B,rho)

[m,n] = size(A);
At = A.^((1./(1-rho))*ones(1,n));

N = 20;   %number of iterations
eps = 1e-4; %tolerance

p = ones(n,1)/n; %initialize prices

P = []; t = [];
for iter = 1:N
    fprintf(1,'Iteration %d of %d...\n',iter,N);
    
    % compute demands
    c = B*p;
    vec = sum(At.*((ones(m,1)*p').^((-rho./(1-rho))*ones(1,n))),2);
    beta = c./vec;
    X = (beta*ones(1,n)).*At.*((ones(m,1)*p').^((-1./(1-rho))*ones(1,n)));
    demand = sum(X,1);
    max_d = max(demand);
    t = [t max_d];
    
    % update prices
    p = p.*(1+(eps/max_d)*demand');
    p = p/sum(p);
    P = [P p];
end

% compute final prices
p = sum(P.*(ones(n,1)*t),2)/sum(1./t);
p = p/sum(p);

% compute final demands
c = B*p;
vec = sum(At.*((ones(m,1)*p').^((-rho./(1-rho))*ones(1,n))),2);
beta = c./vec;
X = (beta*ones(1,n)).*At.*((ones(m,1)*p').^((-1./(1-rho))*ones(1,n)));
    