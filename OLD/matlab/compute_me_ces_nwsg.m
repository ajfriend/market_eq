function [X,p] = compute_me_ces_nwsg(A,B,rho)

[m,n] = size(A);

% Transform A
At = A.^((1./(1-rho))*ones(1,n));
max_rho = max(rho);
t = (1-max_rho)./(1-rho);
q = sum(B,1)';

% Initialize
z = (1/m)*ones(m,1);
sigma = (1/n)*ones(n,1);
MAX_ITER = 200;
epsilon = 1e-7;

iter = 1; EXIT_FLAG = 0;
while ~EXIT_FLAG
	% Current residual
	vec1 = sum((ones(m,1)*(sigma.^(1-max_rho))').*B,2);
	vec2 = sum(At.*((ones(m,1)*sigma').^((-t.*rho)*ones(1,n))),2);
	res = z - vec1./vec2; 
	res = [res;  sum(At'.*(ones(n,1)*z').*((sigma*ones(1,m)).^(ones(n,1)*(1-t'))),2)-q.*sigma];
	if norm(res)<epsilon, EXIT_FLAG=1; end	

	% Compute search direction
	H = [eye(m) -(1-max_rho)*((1./vec2)*ones(1,n)).*B.*((ones(m,1)*sigma').^(-max_rho))-...
		((vec1.*(vec2.^(-2)).*t.*rho)*ones(1,n)).*At.*((ones(m,1)*sigma').^((-rho.*t-1)*ones(1,n)))];
	H = [H; At'.*((sigma*ones(1,m)).^(ones(n,1)*(1-t'))) ...
		diag((((sigma*ones(1,m)).^(ones(n,1)*(-t'))).*At')*(z.*(1-t))-q)];
	
	Delta_x = H\(-res);
	Delta_z = Delta_x(1:m);
	Delta_sigma = Delta_x(m+1:end);

	% Line search
	gamma = 1; %step size
	ind_neg = find(Delta_z<0);
	if ~isempty(ind_neg);
		gamma = min(gamma,0.9*min(-z(ind_neg)./Delta_z(ind_neg)));
	end
	ind_neg = find(Delta_sigma<0);
	if ~isempty(ind_neg)
		gamma = min(gamma,0.9*min(-sigma(ind_neg)./Delta_sigma(ind_neg)));
	end
	
	alpha = 0.001;  delta = 0.5;
	while(1)
		sigman = sigma+gamma*Delta_sigma; zn = z+gamma*Delta_z;	
		vec1 = sum((ones(m,1)*(sigman.^(1-max_rho))').*B,2);
		vec2 = sum(At.*((ones(m,1)*sigman').^((-t.*rho)*ones(1,n))),2);
		res_next = zn - vec1./vec2; 
		res_next = [res_next;  sum(At'.*(ones(n,1)*zn').*...
				((sigman*ones(1,m)).^(ones(n,1)*(1-t'))),2)-q.*sigman];	
		if(norm(res_next) < (1-alpha)*norm(res)), break; end
		gamma = delta*gamma;
	end			
	%gamma = 0.6*gamma;		

	z = z+gamma*Delta_z;
	sigma = sigma + gamma*Delta_sigma;
	fprintf(1,'Iteration: %2d, Residual %e, Stepsize %3.3f\n',iter,norm(res),gamma);
	iter = iter+1;
end
fprintf(1,'Done!\n\n')

p=0; X =0;

% Generate optimal bundles
%X = (beta*ones(1,n)).*At./((ones(m,1)*pn').^((1./(1-rho))*ones(1,n)));
