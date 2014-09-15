# Computing market equilibria via convex optimization
- /home/boyd/papers/market_eq
- Dropbox/sharelatex/market_eq
- https://github.com/ajfriend/market_eq

# Notes
- Border, Kim C. "Fixed point theorems with applications to economics and game theory." Cambridge Books (1990).

- tattonment is a popular algorithm, however, it only converges under gross substitutability assumptions. perhaps ADMM gives a tattonment-like algorithm that works in a relaxed setting.
- look at the welfare adjustment scheme in Codenotti et all 2005. it searches through weightings of the group welfare function to find an equilibrium. how does this connect with duality? is it monotone?
- are any of the non-convex problems monotone?
- weak gross substitutability implies easy cutting planes. monotone?

# Fri Aug 29 12:49:13 2014
- look at the OLD papers. get some history on the arrow-debreu formulation. who did it first?
- look at Market Equilibrium : Resource Allocation Problem, good summary notes.
- different convex formulations: A Rational Convex Program for Linear Arrow-Debreu Markets
- some weird piecewise-linear concave utilities. does this give a convex program? A Perfect Price Discrimination Market Model with Production, and a Rational Convex Program for It

# Sun Aug 31 20:01:40 2014
- solving big problems outside of the convex formulation by nonconvex ADMM? would that work? easy enough to look at convergence
- look at the optimality conditions for an individual agent. can i write down a big program? does this give an easy way to derive the convex formulations for fisher and arrow-debreu? is this what they mean when they talk about the linear complimentarity problem

# Sun Aug 31 23:34:05 2014
- read codenotti 2004 survey
- next to read are jains paper and Market Equilibrium in Exchange Economies with Some Families of Concave Utility Functions

# Mon Sep  1 12:56:57 2014
- you have to look up the infinite convex program references in Jain 2004. it looks like it characterizes for very general utility functions, but the infinite size of the program makes it hard for interior point. however, ADMM might be a good match.
- is gross substitutability a useful concept for the convex formulation?

# Mon Sep  1 23:21:42 2014
- some CES functions work for Arrow-Debreu, but might require a different convex program. look at section 6.4.2 in Algorithmic Game Theory
- also look at Market Equilibrium for CES Exchange Economies: Existence, Multiplicity, and Computation 
- look at CS294 lecture 7 notes. gives CES arrow debreu for -1 <= \rho < 0
- the lecture 7 notes seem to give the arrow-debreu in terms of a demand function for each agent. is this a reasonable convex formulation? would it work for other utilities besides CES?
- does the cutting plane give us something like the infinite LP?
- need to find that infinite LP!

## alternative arrow debreu
- deman functions
- lecture 7 on cs294
- agent optimality conditions
- infinite LP

# Wed Sep  3 21:00:52 2014
## arrow-debreu formulation
- note that \nabla u(x) ^T x is u(x) for homogeneous functions. does this extend what functions work for the arrow-debreu case

## infinite LP
- reading the 2007 version of Jain's paper points out some infinite LP formulations for exchange market for very general utility functions.
- Jain07 points to On the Polynomial Time Computation of Equilibria for Certain Exchange Economies as a good reference
- also maybe look at D. J. Newman and M. E. Primak, Complexity of circumscribed and inscribed ellipsoid methods for solving equilibrium models,
- this might just be the cutting plane interpretation
- i wonder if this scales?

## if this infinite LP/cutting plane method works
- lets just do it, see how it does
- it will probably be slow, but perhaps we can use a heuristic to choose
search directions
- use something like the reweighting of the aggregate social function,
or a convex approximate of arrow-debreu

## jain07
- jain07 gives an exponential or infinite LP or convex program involving cycles in graph
- i think this is different from the classical infinite LP...
- jain also shows that with general concave utilities, the usual Ye characterization is nonconvex, but does capture all the market equilibria
- can we combine this with the infinite LP cutting plane algo?
- of course, with general utilities, the equilibrium may not even be connected
- i think they are only connected when you have gross substitutability

## guy's thesis
- the guys thesis on this stuff actually looks like a really good review of modern approaches.

# Thu Sep  4 19:36:50 2014
## reading On the Polynomial Time Computation of Equilibria for Certain Exchange Economies
- the cutting planes are in the space of price vectors
- but not in the log space we usually deal with in the Jain formulation
- does that cause a problem?
- using sparsity, many goods will be zero (demand and initial), so each agents evaluation will only depend on a subset of prices.
- they use an Ellipsoid method, how well would this do with a cutting plane method?
- we could combine the cutting plane method with convex approximations of
demand to try and get better search directions.

# Fri Sep  5 01:44:40 2014
## its looking very likely that the Excess demand function is monotone
- i think the cutting plane theorem is just a special case of the excess demand operator being monotone
- need to check this
- can we use that in an algorithm?

## tatonnement
- how hard is this computationally, really?
- along with our experiments, we should compare it with tatonnement, which seems like a very natural algorithm that one would think would work well...

# Wed Sep 10 15:06:11 2014
- computational approach. Have user determine type of market and give list of utility functions (objects). the market solver then determines which algorithm or framework to use to solve that market type
- what happens if we take the dual of the fisher formulation? can we get a problem in a smaller parameter space, i.e., just the prices instead of the allocations?
- should i add in a tatonnement section to computational approaches?

# Wed Sep 10 20:18:19 2014
- gives applications of general market equilibrium
J. Whalley J.B. Shoven. Applying General Equilibrium. Cambridge University Press, 1992.

# Thu Sep 11 00:37:41 2014
- a short proof of existence of equilibria can be found in the following book
- existence is a short proof
- it also shows that gross substitutability implies unique prices
Microeconomic analysis
Varian, Hal R.
3rd ed. - New York : Norton, 1992.
Business Library
Today's hours: 8a - 5p
Stacks
 Available HB172 .V35 1992
 Available HB172 .V35 1992

# Thu Sep 11 16:56:44 2014
- read varian chapter 31 from pdf
- read kreps pdf chapter 6

# Fri Sep 12 11:32:45 2014
## good books summary
- varian (grad and undergrad books)
- microeconomic theory by mas-colell, whinston, green
- competitive equilibrium by ellickson
- microeconomic theory by luenberger
- a course in microeconomic theory by kreps

## walras' law
the value of the aggregate excess demand is zero

## mccune thesis
- check out smale's work on newton methods for the problem... woah, its from 1976

# Sun Sep 14 22:30:25 2014
- in the exchange model, if we use the welfare setting and are trying to find the unknown weights, but agents have homogeneous utility functions, is it the case that the weights end up being exactly how much money they get from selling their initial endowment, just like in the fisher convex program?
- can we alternate between prices and weights to get a nice algorithm?
- is the set of weights convex?

# Sun Sep 14 22:59:26 2014
- what about splitting buying and selling into different prox operators
- it jives nicely as a way to move between fisher and arrow-debreu settings
- could simplify the prox operators enough to not need an EXP solver

