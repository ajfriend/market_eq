import numpy as np
import cvxpy as cvx
from itertools import izip
from market_eq import helper


'''
How to handle endowments for fisher and arrow-debreu markets?
can i just have a good called 'money'?
how do i ignore that good when doing arrow-debreu?
separate classes?
- use __slots__ for agents and functions to save space?
'''

"""
- proxer takes in an object or set of objects that give constraints and
objectives. the proxer then forms the prox and evaluates it. we can use this
to group agents together, if we want more than one in our prox
- TODO: agent's should have an interface to construct their constraints.
would make the proxer code much cleaner
- TODO: use `views` on dicts to intersect keys and items without having to
make a list or set
- TODO: what if i want to start the iteration near a solution?
- todo: could also add good constraints into proxers
- todo: overstepping? good initialization?
"""


def agent_validator(agent_init):
    def new_init(self, util_fn, goods, b):
        if len(goods) != len(b):
            raise Exception('goods and b vectors must have the same length.')

        if len(goods) == 0:
            raise Exception('Agents need nonzero initial endowment.')

        # check that the initial endowment goods are all positive
        for k in b:
            if k <= 0:
                raise Exception('Endowment goods must be positive.')

        agent_init(self, util_fn, goods, b)
    return new_init


class Agent(object):
    __slots__ = 'util_fn', 'goods', 'b'

    @agent_validator
    def __init__(self, util_fn, goods, b):
        """
        :param goods: the keys for the initial endowment of goods
        :param b: the associated amounts of initial endowment
        :param util_fn: the agent's utility function
        :return:
        """
        self.util_fn = util_fn
        self.goods = np.array(goods)
        self.b = np.array(b)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Agent({},{},{})".format(self.util_fn, self.goods, self.b)

    def log_cash(self, phi):
        tmp = [np.log(b) + phi[g]
               for g, b in izip(self.goods, self.b)]
        tmp = cvx.log_sum_exp(cvx.vstack(*tmp))
        if tmp.is_constant():
            return tmp.value
        else:
            return tmp

    def demand(self, phi):
        log_cash = self.log_cash(phi)
        return self.util_fn.demand(phi, log_cash)

    def constr(self, x, phi):
        return self.util_fn.constr(x, phi, self.log_cash(phi))

    def eval_util(self, x):
        return self.util_fn.eval(x)

    def displeasure(self, x, phi):
        util_star, _ = self.demand(phi)
        util_0 = self.eval_util(x)

        return max(0, 1 - util_0/util_star)

    @staticmethod
    def rand(util_type, n, k, a_ind, b_ind):
        """
        Make a random agent with util_type utility function.
        Interested in k of n goods for purchase. (a_ind required indices)
        Selling k of n goods. (b_ind required indices)
        """
        util = util_type.rand(n, k, a_ind)
        b_keys = helper.rand_tuple(n, k, b_ind)
        b_amount = np.random.rand(k)

        return Agent(util, b_keys, b_amount)
