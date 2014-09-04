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

# viz
- http://www.madhavajay.com/kalki/
- http://physics.stackexchange.com/questions/5569/is-there-a-nice-tool-to-plot-graphs-of-paper-citations
- search: "google scholar graph"
- http://academic.research.microsoft.com/
- http://anrope.com/blog/2011/05/11/hey-google-scholar-where-is-my-citation-visualization-tool/
- http://www-personal.umich.edu/~ferraris/googlescholarvisualization.html
- http://hublog.hubmed.org/archives/001002.html