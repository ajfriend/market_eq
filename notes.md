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

# Mon Sep 15 03:07:03 2014
- look at [multiplier to residual mapping notes](http://stanford.edu/class/ee364b/lectures/monotone_slides.pdf)
- can we use the same technique to show that the demand function is monotone?

# Mon Sep 15 22:12:04 2014
- what are the conditions for arrow-debreu 1954. only quasi-concave!?, and nonsatiatable? is the last really necessary?
- eisenberg and gale's fisher result only depends on concavity and homogeneity.
- the homogeneity comes from the fact that we don't want to punish a buyer if he splits into 2 buyers with half the money. is there a way to generalize that?
- show CES computability line from lecture 15 and make sure you're citing the papers
- look into last slides of lect 15 for WARP

# Mon Sep 15 23:34:00 2014
## monotone papers
# Mon Sep 15 23:31:33 2014
- the monotone folder in the papers directory has the relevant papers
- also look at Equilibrium Theory and Applications. it has a chapter by Mas-Colell
- green library has it: HB145 .I59 1989

# Tue Sep 16 15:34:24 2014
## looking at a whole bunch of books from green
- numerical methods in economics by judd mentions the arrow-debreu problem, but doesn't really solve it. 
- Equilibrium Theory and Applications has a chapter by Mas-Colell. green library has it: HB145 .I59 1989. goes over monotone operators.

# Wed Sep 17 01:48:57 2014
- most of the utility functions are covered by the two cases given by Ye. it just requires a monotone transformation
- ye gives two papers to reference that leonteif utilities are np hard for exchange
- what about sums of utilities?
- are the only poly time algos for -1 < rho < 0 from Codenotti?

# Thu Sep 18 15:30:06 2014
- optimality conditions for a single guy in arrow-debreu
- ye's derivation of the global system

# introduction
# prioor work
# solution via exponential cone solver
# 

convex/concave. find a saddle point in x,p
augmented lagrangian in u

max u(x) + lambda p^t x + 1/2 || p - z ||^2

something like the above might give you what you want to comptue the resolvent.

papers dir for prox stuff. something about convex/concave proxes and
finding saddle points.

write the abstract first. exploiting sparsity. splitting.

# Sat Sep 20 17:25:30 2014
- substitute out x, since you have the resolvent constraint involving p and q and w.
- get a non-convex constraint, but we might be able to work around it
- is it justified to just constrain p to be in the simplex? that keeps it from making p too small
- what about stephens augmented lagrangian method?
- look at the monotone notes for when a differentiable map is monotone
- look at this saddle point characterization in the notes

# Mon Sep 22 01:58:15 2014
- switch to biblatex?

# Tue Sep 23 22:48:27 2014
- i'm comfortable with the fisher equilibrium conditions and transformations, and the proof (at least in the linear case) that the aggregate program gives the equilibrium
- general fisher case?
- aggregate requires homogeneous utilities?
- i can see the transformation which is made to remove the non-convex constraint. how does that generalize for arrow-debreu?
- can i do a conjugate form of arrow-debreu and fisher?

# Wed Sep 24 00:05:15 2014
- why do the fisher opt conditions require the extra constraint?
- can i not just do the arrow-debreu setting once, and fisher is a speical case?
- we'll have to see if the conjugate actually helps, since the dual gap constraint usually just goes into removing a dual variable.

# Thu Sep 25 01:14:13 2014
## object oriented design
- list for utility interests (ordered)
- dictionary for initial endowment (ordered?)
- each of these should have keys for goods. keys can be anything in python
- function for mapping between good dictionary and contiguous array for utility function
- interface for utility function includes evaluation, log u^T x, log u
- utility function interface plugs into a common prox function code
- emits dict of prox result
- aggregator does average and sends it back out
- the individual proxes can limit the number of constraints based on their expectation of what will be active
- maybe we can even do multiple iterations until we get it right
- or maybe we get it wrong initially, and let ADMM sort it out in the limit
- should do this in a general way, to allow for both GS cutting plane method and Fisher version.
- the object should be able to take in a dict which contains *everything*, but it won't read it all. it just requires that the dict has at least what it is specifying.

# Sun Sep 28 14:30:12 2014
- make a market object which collects agents
- fisher and arrow-debreu market types
- allow it to check that the market is reasonable: each good wanted, each person wants
- allow the market to compute equilibrium
- returns a consensus algorithm object? with residual info over the runs of the algo? allow it to warm start, so we can tack on 100 extra iterations, if we want
- we can apply different algorithms to a market: tatonnment, aggregate re-weighting, cutting plane, admm

# Mon Sep 29 16:54:52 2014
- 'ULD' property from page 111 in Mas-Colell is exactly *monotonicity*

# Fri Oct  3 17:50:28 2014
- i just need a key-value averager
- how do i generalize for multiple variable types? (x, phi)?
- what about an efficient double dict for row, column sums?
- is it simpler to have a single proxer for each agent?
- who takes care of forming the input to the prox? same prox object? data-prep function, or wrap the proxer in another class?

# Tue Oct  7 01:55:35 2014
- for places to publish, look at GAMS and other 'commonly used' packages in microeconomics to see what is being done and how.

# Wed Oct  8 13:47:08 2014
- walras' law is just that the entire consumer budget is spent.
- demand function (of prices and consumer wealth) should be homogeneous of degree 0
- the above two assumptions are very general.
- GS is a bit restrictive.
- look at ex 2.f.13 in mas-collel
- is there a relation between monotone operators and strongly monotone preference relations?

# Wed Oct  8 17:18:06 2014
- i think GS implies WARP?
- gs gives a cutting plane. does warp give the same cutting plane?
- kehoe does some experiments. but the implication seems to be warp => gs... werid
- why do they say that warp can hold for agents, but possibly not in aggregate?
- perhaps there is some detail about the price domain not being full. we are restricted to the positive price simplex?
- i need to look at the example where it does not hold in mas-collel...

# Wed Oct  8 21:30:00 2014
- chapter 2 and 4 here are good notes <http://business.illinois.edu/nmiller/notes.html>

# Thu Oct  9 12:16:15 2014
- i think the question is wether this operator is *maximal* monotone. can we extend the prices to all of R^n?
- can i write a test for the utility funcs to compare the demand function with the optimization code. want both to be feasible allocations and have close utility values.

# Mon Oct 13 21:05:14 2014
- introduce nicer, cleaner definitions into the first introduction section explaining the markets
- give demand and excess demand functions
- in the definitions section, give GS, WARP, and maybe monotone
- add in proof of optimality of arrow-debreu as appendix.
- - really good looking notes on variational ineq and monotone ops: <http://supernet.isenberg.umass.edu/courses/SCH-MGMT825-Spring14/VI_Lecture1_Nagurney.pdf>

# Tue Oct 14 23:24:05 2014
- go through mas-collel notes again
- review early codenotti papers and mccune thesis
- On the Polynomial Time Computation of Equilibria for Certain Exchange
- Market Equilibrium in Exchange Economies with Some Families of Concave Utility Functions

## monotonicity papers
- PSEUDOMONOTONE FUNCTIONS AND
AN APPLICATION IN THE THEORY OF GENERAL ECONOMIC EQUILIBRIUM
- On Revealed Preference Analysis
- On the uniqueness of equilibrium once again

# Tue Oct 28 13:21:59 2014
- problem, properties, 
    - utilities
- numerical methods
    - cvxpy
    - distributed
- examples

clarify how many problems, how many utilities

problem, utilities, is it solvable.

# Wed Oct 29 16:25:03 2014
remember to check
- <http://www.cs.berkeley.edu/~christos/agt11/notes/lect7.pdf>
- <http://people.csail.mit.edu/costis/6853fa2011/6853-Lecture16.pdf>

# Sun Nov 23 16:43:28 2014
- look at nesterov and socp paper
- how does nesterov do the normal (unweighted) geo mean? 1/n case?

log scale plot

how to make problems, 10 random instances

centralized alg
distributed alg

3 pages

ecos/scs: n vs solve time

iters and residual for distributed alg

one problem for big.

we check correctness.

fig 2 (exactly two figures)
to illustrate convergence of alg, solve problem instance of size 10^6.

1 million users/ 1 millino goods, soak it in.
data alone was 2gb to describe.

average vs worst case residual. 

each iteration required 4 minutes on kona64

examples
1.1 how to make random problems
1.2 centralized
1.3 decentralized

maybe some dense ones in figure 1, combined with the sparse ones. (maybe separate plot)
http://users.isy.liu.se/johanl/yalmip/pmwiki.php?n=Tutorials.NonlinearOperators
http://users.isy.liu.se/johanl/yalmip/pmwiki.php?n=Tutorials.GraphRepresentations

# Mon Dec  1 22:53:17 2014
- make sure to note *why* the problem is hard, exponential cone
- in the map-reduce step, make sure we handle division by zero correctly

# Tue Dec  2 16:40:20 2014
## for applications look at
- shoven  Available HB145 .S53 1992 green
- Equilibrium theory and applications : proceedings of the Sixth International Symposium in Economic Theory and Econometrics   HB145 .I59 1989 green
- look through my collected papers

# Thu Dec  4 14:57:17 2014
- how to consistently refer to the formulations for exchange and fisher? by equation? or by section? formulation or algorithm?
- figure out how to reference secitions, write out section, or use section symbol?
- what about the proofs? maybe just exchange? what about fisher?
- CES context reference?
- for fisher, add ref that any ___ function can be tranformed to homogeneous of deg 1
- leonteif, add ref that you get disconnected equilibria
- what to do with piecewise linear? combine with leonteif?
- fractional power and log - given by ye to give context
- for log and frac power, need better nomenclature for the types of formulations and algorithms we can use with fisher and exchange problems.
- compare with GAMS?
- recent updates: Algorithms for Equilibrium Prices in Linear Market Models
Kurt Mehlhorn
- will the algorithmic case of no prices (for fisher) be automatically taken care of? do we lose any algorithmic efficiency?
- make sure consistent use of forall and \ldots
- it is decided: use \S for section references `\S\ref{s-content}`
- figures are done like `Figure~\ref{f-nopsfrag}`
- equivalence when prices are nonzero, *sane* markets
- for a justification of the equality, see appendix a
- periods at the ends of paragraph tags
- "we will refer to these as the fisher formulation and the exchange formulation, respectively." note that an exchange problem must be solved using the exchange formulation, but a fisher problem may be solved by either formulation, depending on the utility functions, by transforming it into an exchange problem.

we will introduce the individual problem of agents, the equilibrium problem of brining the agents' demands in line with supply, by defining these problems mathematically, we will then give various *formulations* to solve these problems.
we will define both fisher and exhcange problems,

then we give some computational frameworks for computing solutions to these convex problems, and provide examples.