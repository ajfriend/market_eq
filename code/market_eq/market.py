from collections import defaultdict, Counter

import numpy as np

from market_eq import utility as util
from agent import Agent
from itertools import izip
import random


def gen_market(n, r, seed=None):
    """ Generate a market with n agents and n goods,
    with each agent interested in r goods, and endowed with r goods.
    Arranged so that each good is wanted by someone, provided by someone.
    """
    assert r <= n
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    # goods interested in
    a = np.random.permutation(n)
    # initial endowment
    b = np.random.permutation(n)

    market = Market()
    for a_ind, b_ind in izip(a, b):
        #util_fn = random.choice([util.Linear, util.CES, util.CobbDouglas])
        #util_fn = util_fn.rand(p, n)
        #util_fn = util.Linear.rand(n, r, a_ind)

        agent = Agent.rand(util.Linear, n, r, a_ind, b_ind)
        market.add(agent)

    print 'goods: ', len(market.goods), ' agents: ', len(market.agents)
    print "market is sane: ", market.sane()
    print "market is really sane: ", market.really_sane()

    return market


class Market(object):
    """check that every good is desired, everyone desires something,
    and goods desired by someone other than owner"""

    def __init__(self, agents=None):
        self.agents = set() if agents is None else set(agents)

    def add(self, agent):
        """add an agent to the market"""
        self.agents.add(agent)

    @property
    def goods(self):
        """dict: find all the goods available in the market and the total
        available amount"""
        d = Counter()
        for a in self.agents:
            d.update(dict(zip(a.goods, a.b)))

        return d

    @property
    def desired(self):
        """return the desired goods with a count of agents interested in
        that good"""
        d = Counter()
        for a in self.agents:
            d.update(a.util_fn.goods)

        return d

    def sane(self):
        """ Test that the set of desired goods is equal to the set of
        available goods.
        """
        return set(self.goods.viewkeys()) == set(self.desired.viewkeys())

    def really_sane(self):
        """ Return the goods desired by at least one agent other than the one
        who owns it. if two agents both own and desire the same good,
        then this should still pass.
        TODO: i think we can generalize this. higher orders of this question
        are something like if there graph is a single strongly connected. if
        not, we can split into non-interacting sub-markets. use a graph
        algorithm to check.
        """
        offered = set()
        desired = set()
        paired = set()

        for a in self.agents:
            # this agent wants and someone else is offering
            paired.update(set(a.util_fn.goods) & offered)
            # this agent is offering and someone else wants
            paired.update(set(a.goods) & desired)

            offered.update(a.goods)
            desired.update(a.util_fn.goods)

        return paired == offered and paired == desired

    #todo update
    def check_sol(self, xs, phi):
        """ tuple of violations of the proposed solution given by xs and phi.
        tuple gives *positive* violations to good positivity, global good
        constraints, and violations to the convex programming formulation
        constraints
        """
        min_val = +np.Inf
        good_viol = {g: -v for g, v in self.goods.iteritems()}
        max_viol = -np.Inf
        for a, x in xs.iteritems():
            min_val = min(min_val, min(x.itervalues()))
            for g, v in x.iteritems():
                good_viol[g] += v

            # compute the utility constraint violations
            max_viol = max(max_viol, max(a.constr(x, phi)))
        good_viol = max(0, max(good_viol.itervalues()))
        return max(-min_val, 0), good_viol, max_viol

    # todo update
    def polish_sol(self, xs, phi):
        """ Polish a proposed solution given by xs and phi.
        Changes xs and phi *in place*.
        the log prices, phi, should sum to 0.
        We take the positive part of each good allocation, and then
        normalize the goods so that they sum to the correct amount.
        """

        # phi should sum to zero
        t = sum(phi.values())/len(phi)
        for g in phi:
            phi[g] -= t

        good_total = defaultdict(float)
        good_avail = self.goods

        for a, x in xs.iteritems():
            for g, v in x.iteritems():
                v = max(v, 0)
                x[g] = v
                good_total[g] += v

        for a, x in xs.iteritems():
            for g, v in x.iteritems():
                try:
                    x[g] = v*good_avail[g]/good_total[g]
                except ZeroDivisionError:
                    raise ZeroDivisionError('On key: {}'.format(g))

    def displeasure(self, xs, phi):
        out = []
        for a in self.agents:
            out.append(a.displeasure(xs[a], phi))

        return np.mean(out)

    def __str__(self):
        return "".join(str(self.agents))
