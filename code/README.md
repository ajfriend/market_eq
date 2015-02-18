# Market Equilibrium
compute market equilibrium

## config
I added `market_eq.pth` to `usr/local/lib/python2.7/site-packages` to make
the market_eq stuff findable.
- `ipcluster start -n 4`

## Running `nosetests`
- run `nosetests test/test2.py` from the top market_eq directory
- `-v` option for verbosity
- `-s` option to turn off output capture

## affinity with numpy in Ipython parallel
- [link](http://stackoverflow.com/questions/16323743/ipython-parallel-not
-using-multicore)
- [notebook discussing processor affinity](http://nbviewer.ipython
.org/gist/minrk/5500077)
- [good ipython parallel tutorial](http://www.astro.washington
.edu/users/vanderplas/Astr599/notebooks/21_IPythonParallel)
- [interesting blog post](http://continuum.io/blog/ipcluster-wakari-intro)
- [numba tips](http://continuum.io/blog/numba-tips)


## todos
- make util_funcs and agents (and markets?) immutable objects
- maybe use slots to save memory for utility functions and agents?
- dict iteration is always in the same order if you don't change the keys. 
shouldn't need to use OrderedDict, although it is an option.
- use `__slots__` or `namedtuple` to save memory?
- replace `dict`s with `namedtuple`s to save memory and time?
- to save memory and time, maybe use tuples inside utility functions and 
agents. these objects are not mutable. we can still have the public
interface involve dicts tho, since that is convenient.
- would such an interface solve the ordering problem (by giving a default 
ordering) for stuffing the cvxpy parameters?
- move the random util func generation into the util funcs, but add
the possibility of defining a set of must-have goods.
- we can make the solution polishing distributed. just need to broadcast the
 scaling factor. each proxer can do the clipping itself.
 - can i just use Counter dicts to simplify the addition and division 
 operators?
 - publish examples on wakari!


## notes
- by default, user defined objects hash to their memory id: `id()`
- can i make identical agents? do i want to?
- for keys, do `dict`s store an object reference?

- we will allow the agents to be id' and hashed by their `id()` since
two agents can have the same data, but shouldn't be identified as the same 
agent
- use integer keys for goods to save space
- we might be able to just pass around a single numpy array instead of a dict




## distributed design
- make a random agent constructor (supply it with the util type, 
number of goods, endowment, and required indices)
- make the efficient fixed-dict thing. it should be instant access when the 
dict is contiguous (full size)
- don't need agent ids; only within the accountant do we need to manage that.
inside there, it is ok to have a dict for the agents
- use the efficient dict for aggregating amounts and counts of the prox. 
precompute before sending to central location
- agent and util interface should always remain as dicts. (can i make sure 
they work with arbitrary keys?)
- the idea is to only use the integer keys for the large-scale algorithm
- will the efficient dict work with cvxpy arrays?
- the distributed code should work basically the same within or without 
ipython.parallel. just maps, applys, list comprehensions and reductions.
- can use the efficient dict for xtild and for phibar (these are the only
things sent down to the accountants)
- accountants don't send back agent ids, they only send back results
- if we really want an agent corresponding to final solution, 
we can always pull it back
- the efficient dict (numpy arrays) for the partial aggregates at the machine
level know their keys ahead of time, since they do not change iteration to 
iteration.
- move the code for generating random stuff (and probably the efficient dict)
into *another* utility module.
- if we really want fast insertions, we can create a one-time lookup table
(which we don't store in the object, so that we don't send it over the network)

- what is the ECOS trick jack is thinking about?
- seems to be same as iterative refinement. is it not true that it always 
converges?
- adding diagonal regularization with the intent of using iterative refinement
to solve systems efficiently, without having to do a lot of work factoring


## sparse dict
- d.max(0) could max(elem,0) with eleverything inside
- could nest them to do the updating in Accountants
- could mulitply with constant for scaling
- d >= 0 can return true or false and be recursive (maybe return cvxpy 
constraints?)
- 
