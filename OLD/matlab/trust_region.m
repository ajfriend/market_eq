%% Trust region method for Arrow-Debreu market equillibrium
clear all; close all
cvx_quiet(true);
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

delta_max = .1;  %trust region width
psi = zeros(n,1); %initial price vector

%% Main trust-region loop
agent_res = [];
market_res = [];
MAX_ITER = 300; tol = 1e-8;
tic 
for iter = 1:MAX_ITER
    
    %Compute step via QP
    cvx_begin
        variables X(m,n) delta_psi(n,1) t(m,1)
        maximize(min(t))
        subject to
            sum(delta_psi)==0;
            norm(delta_psi,Inf)<=delta_max;
            X>=0;
            D1=(B*exp(psi))*(exp(-psi).*(1-delta_psi))';
            D2=B*(exp(psi).*delta_psi)*exp(-psi)';
            t*ones(1,n)<=sum(A.*X,2)*ones(1,n)-A.*(D1+D2)+(A.*B).*(ones(m,1)*delta_psi');
            sum(X,1)==sum(B,1);
    cvx_end
    
    %Update prices
    psi = psi+delta_psi;
    
    %Calculate new residual
    res = min(sum(A.*X,2)-max(A.*((B*exp(psi))*exp(-psi)'),[],2))
    agent_res = [agent_res res];
    
    if res>-tol, break; end
end
toc

figure
semilogy(agent_res,'LineWidth',2)
set(gca,'FontSize',15)
ylabel('agentres')
xlabel('iter')
%print -depsc agent_res.eps

X = round(X*10^5)*10^(-5);
figure
spy(X)
xlabel('goods')
ylabel('agents')
%print -depsc sparsity.eps
