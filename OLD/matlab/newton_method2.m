%% Trust region method for Arrow-Debreu market equillibrium
clear all; close all
%rand('state',0)

% Generate data
m = 10; %number of agents
n = 10; %number of goods
pA = 0.01; pB = 0.01;
indA = (rand(m,n)<pA);
indB = (rand(m,n)<pB);
A = rand(m,n); %utility matrix
B = rand(m,n); %initial budget
%A = A./(sum(A,2)*ones(1,n));
%B = B./(ones(m,1)*sum(B,1));
%A = sparse(A.*indA);
%B = sparse(B.*indB);

%rho = 0.7*rand(m,1)+0.1;
%rho = 0.9*ones(m,1);
%rho = 2*rand(m,1)-1;
rho = -rand(m,1);
%eps= 0.1;
%rho = (2-eps)*rand(m,1)-1;

tic
[X,p] = compute_me_ces(A,B,rho);
U = sum(sum(A.*(X.^(rho*ones(1,n))),2).^(1./rho));
toc

tic
[X2,p2] = compute_me_walg(A,B,rho);
U2 = sum(sum(A.*(X2.^(rho*ones(1,n))),2).^(1./rho));
toc