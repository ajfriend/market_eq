%% Projected subgradient method for Arrow-Debreu market equillibrium
%clear all; close all
rand('state',0)

% Generate data
m = 10; %number of agents
n = 10; %number of goods
pA = 0.4; pB = 0.4;
indA = (rand(m,n)<pA);
indB = (rand(m,n)<pB);
A = rand(m,n); %utility matrix
B = rand(m,n); %initial budget
A = A.*indA;
B = B.*indB;

%return

% Initialize
X = ones(m,1)*sum(B,1)/m;
psi = zeros(n,1);

% Main loop
MAX_ITER = 5000; agent_res = []; res_best = inf;
for iter = 1:MAX_ITER
    if mod(iter,1000)==0
        iter
    end
    % Compute agent residual
    C=-sum(A.*X,2)*ones(1,n)+A.*(ones(m,1)*exp(-psi)').*((B*exp(psi))*ones(1,n));
    res = max(C(:)); 
    agent_res = [agent_res min(res,res_best)];
    res_best = min(agent_res);
    [I,J] = find(C==res);
    index = randperm(length(I));
    I = I(index(1)); J = J(index(1));
    
    % Step Size
    alpha = 0.2/sqrt(iter);
    %alpha = 0.1;
    
    % Compute subgradient and take step
    dX = zeros(m,n); dX(I,:) = -A(I,:);
    dpsi = A(I,J)*exp(-psi(J))*exp(psi).*(B(I,:)');
    dpsi(J) = dpsi(J)-A(I,J)*exp(-psi(J))*(B(I,:)*exp(psi));
    X = X-alpha*dX;
    X(X<0) = 0;
    psi = psi-alpha*dpsi;
    
    % Project solution by water filling
    cs = sum(B,1);
    for l = 1:n
        c = cs(l); y = X(:,l);
        delta = sum(y)-c; k = m; x2 = y;
        while(delta~=0)&&(k>1)
            ind = x2; ind(x2==0) = inf;
            x2 = x2 - min(min(ind),delta/k)*ones(m,1);
            x2(x2<0) = 0;
            k = k-1;
            delta = sum(x2)-c;
        end
        X(:,l) = x2;
    end
    psi = psi-mean(psi);
end
        
    
    