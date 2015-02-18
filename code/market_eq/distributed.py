import numpy as np
from itertools import izip
import market_eq.utility as util
from market_eq.agent import Agent

from IPython.parallel import Reference

# todo: make a dist_market object? can have the same interface as the
# centralized market?


def dist_market_gen(dv, n, r, prox_size=1):
    # goods interested in
    a = np.random.permutation(n)
    # initial endowment
    b = np.random.permutation(n)

    dv.scatter('a', a, block=True)
    dv.scatter('b', b, block=True)
    dv['agents'] = set()

    dv.apply_sync(form_agents, n, r, Reference('a'), Reference('b'), Reference(
        'agents'))
    dv.execute('del a', block=True)
    dv.execute('del b', block=True)

    with dv.sync_imports():
        from market_eq.solvers.admm_solver import ADMMController

    ar = dv.execute('acc = ADMMController.split_agents(agents,prox_size={})'.format(prox_size))
    return ar

# for a set of agents, and a max proxer size of k, split them into proxers
# take the modulus to evenly distribute
# how to keep track of the agent's identities?
# how to distribute data properly?


def form_agents(n, r, a, b, agents):
    """
    Add new agents to agents
    :param n: the number of total goods
    :param r: number goods interested in and supplying
    :param a: required indices for utils
    :param b: required indices for endowment
    :param agents: the set to add the agents to
    :return:
    """
    for a_ind, b_ind in izip(a, b):
        #util_fn = random.choice([util.Linear, util.CES, util.CobbDouglas])
        #util_fn = util_fn.rand(p, n)
        #util_fn = util.Linear.rand(n, r, a_ind)

        agent = Agent.rand(util.Linear, n, r, a_ind, b_ind)
        agents.add(agent)




