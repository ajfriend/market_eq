function [X,p] = compute_me_ces(A,B,rho)

[m,n] = size(A);

% Transform A
At = A.^((1./(1-rho))*ones(1,n));

% Initialize
p = ones(n,1);
beta = ones(m,1);
MAX_ITER = 200;
epsilon = 1e-7;

iter = 1; EXIT_FLAG = 0;
while ~EXIT_FLAG
	% Current residual
	res = (((p*ones(1,m)).^(ones(n,1)*(-1./(1-rho')))).*At')*beta...
		-sum(B,1)';
	res = [res; sum(At.*((ones(m,1)*p').^((-rho./(1-rho))*ones(1,n))),2).*beta-...
			B*p];
    %res = [res; sum(p)+sum(beta)-n-m];
	if norm(res)<epsilon, EXIT_FLAG=1; end	

	% Compute search direction
	H = [(At.*((ones(m,1)*p').^((-1./(1-rho))*ones(1,n))))' ...
		diag(((ones(n,1)*(-1./(1-rho'))).*((p*ones(1,m)).^(ones(n,1)*(-2./(1-rho')))).*At')*beta)];
	H = [H; diag(sum(At.*((ones(m,1)*p').^((-rho./(1-rho))*ones(1,n))),2)) ...
		(((-rho./(1-rho)).*beta)*ones(1,n)).*At.*((ones(m,1)*p').^(((1-2*rho)./(1-rho))*ones(1,n)))-B];
	%H = [H; ones(1,m+n)];
    Delta_x = H\(-res);
	Delta_beta = Delta_x(1:m);
	Delta_p = Delta_x(m+1:end);

	% Line search
	gamma = 1; %step size
	ind_neg = find(Delta_beta<0);
	if ~isempty(ind_neg);
		gamma = min(gamma,0.99*min(-beta(ind_neg)./Delta_beta(ind_neg)));
	end
	ind_neg = find(Delta_p<0);
	if ~isempty(ind_neg)
		gamma = min(gamma,0.99*min(-p(ind_neg)./Delta_p(ind_neg)));
	end
	
	alpha = 0.01;  delta = 0.5;
	while(1)
		pn = p+gamma*Delta_p; betan = beta+gamma*Delta_beta;
		res_next =(((pn*ones(1,m)).^(ones(n,1)*(-1./(1-rho')))).*At')*betan+...
			-sum(B,1)';
		res_next = [res_next; sum(At.*((ones(m,1)*pn').^((-rho./(1-rho))*ones(1,n))),2).*betan-...
			B*pn];
		if(norm(res_next) < (1-alpha)*norm(res)), break; end
		gamma = delta*gamma;
	end			

	beta = beta+gamma*Delta_beta;
	p = p + gamma*Delta_p;
	fprintf(1,'Iteration: %2d, Residual %e, Stepsize %3.3f\n',iter,norm(res),gamma);
	iter = iter+1;
end
fprintf(1,'Done!\n\n')

% Generate optimal bundles
X = (beta*ones(1,n)).*At./((ones(m,1)*pn').^((1./(1-rho))*ones(1,n)));
