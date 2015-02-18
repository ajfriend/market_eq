from collections import defaultdict, Counter
import cvxpy as cvx
from market_eq.agent import Agent
import math
from itertools import izip
from market_eq.market import Market
from IPython.parallel import Reference


class AvgCounter(object):
    def __init__(self):
        self.val = Counter()
        self.count = Counter()

    def add_vals(self, d):
        for g, val in d.iteritems():
            self.val[g] += val
            self.count[g] += 1

    def add_counter(self, avgcount):
        for g, count in avgcount.count.iteritems():
            self.val[g] += avgcount.val[g]
            self.count[g] += count
        return self

    def avg(self, offset=None):
        val = Counter(self.val)
        if offset is not None:
            val.subtract(offset)
        return {key: val[key] / float(self.count[key]) for key in self.count}

    def scale(self, b):
        scale = {}
        for g, val in self.val.iteritems():
            scale[g] = b[g] / val

        return scale

    @staticmethod
    def reduce_tuple(tups):
        result = None
        for tup in tups:
            if result is None:
                result = [AvgCounter().add_counter(c) for c in tup]
            else:
                for r, c in izip(result, tup):
                    r.add_counter(c)

        return tuple(result)


def dummy_step(acc, xtild, phibar, u):
    return acc.step(xtild, phibar, u)


def dummy_displeasure(acc, scale, phibar):
    return acc.displeasure(scale, phibar),


class DistADMM(object):
    def __init__(self, dv):
        self.dv = dv

        self.xtild = defaultdict(float)
        self.phibar = defaultdict(float)
        self.u = defaultdict(float)

        self.b = Counter()
        for agents in dv['agents']:
            for agent in agents:
                self.b.update(dict(zip(agent.goods, agent.b)))

    def step(self):
        xs_count, phi_count = AvgCounter.reduce_tuple(self.dv.apply(
            dummy_step, Reference('acc'), self.xtild,
                     self.phibar,
                 self.u))

        self.xtild = xs_count.avg(self.b)
        self.phibar = phi_count.avg()
        for g in self.u:
            self.u[g] += self.xtild[g]


        scale = xs_count.scale(self.b)

        # todo: might not need apply sync here...
        result = self.dv.apply_sync(dummy_displeasure, Reference('acc'), scale,
                               self.phibar)
        disp_count, = AvgCounter.reduce_tuple(result)

        return disp_count.avg()['disp']

    def solve(self, iter=5):
        for k in range(iter):
            yield self.step()


class ADMMController(object):
    # either has accountants, or dv, with each of those having accountants
    # maybe split this into two classes
    # also allow for a distMarket class
    def __init__(self, market, prox_size=1):
        if isinstance(market, Market):
            self.accts = [ADMMController.split_agents(market.agents,
                                                      prox_size)]
        else:
            raise Exception("Not a recognized market type.")

        self.market = market

        self.b = market.goods

        self.xtild = defaultdict(float)
        self.phibar = defaultdict(float)
        self.u = defaultdict(float)

    # first, write this for the centralized case
    def step(self):
        xs_count, phi_count = AvgCounter.reduce_tuple(acc.step(self.xtild,
                                                       self.phibar, self.u) for acc in self.accts)

        self.xtild = xs_count.avg(self.b)
        self.phibar = phi_count.avg()
        for g in self.u:
            self.u[g] += self.xtild[g]


        scale = xs_count.scale(self.b)

        disp_count, = AvgCounter.reduce_tuple((acc.displeasure(scale,
                                                            self.phibar),) for acc
                                 in self.accts)

        return disp_count.avg()['disp']

    # do repeated calls to solve continue the admm iteration?
    def solve(self, iter=5):
        for k in range(iter):
            yield self.step()


    @staticmethod
    def split_agents(agents, prox_size):
        """
        Returns an accountant containing some proxers.
        """
        n = len(agents)
        num_proxers = int(math.ceil(float(n) / prox_size))

        sub_agents = [set() for _ in xrange(num_proxers)]
        for i, agent in enumerate(agents):
            sub_agents[i % num_proxers].add(agent)

        return Accountant([Proxer(lst) for lst in sub_agents])


# todo: slots this guy
class Accountant(object):
    """ Wraps multiple proxers to do ADMM updating math.
    todo: UPDATE: wrap multiple proxers, one accountant per compute node
    todo: untangle the step and dissatisfaction code. get it working,
    separate functions. displeasure works on the state of the current admm
    aggregator and the state of the accountants. we can interleave them
    later once it is working.
    """
    # does not keep track of u
    # keeps track of w
    def __init__(self, proxers):
        self.proxers = set(proxers)

        # each proxer has a w variable
        self.w = {}
        for p in self.proxers:
            self.w[p] = dict.fromkeys(p._phi.viewkeys(), 0.0)

        # key xs by agent
        self.xs = defaultdict(lambda: defaultdict(float))

        # key phi by proxer
        self.phi = defaultdict(lambda: defaultdict(float))

    def step(self, xtild, phibar, u):
        # todo: can i subclass Counter or make a sparse vector dict object
        # to simplify these formulas?
        # self.w += self.phi - phibar
        xs_count = AvgCounter()
        phi_count = AvgCounter()
        for proxer in self.proxers:
            for g in self.w[proxer].viewkeys():
                self.w[proxer][g] = self.w[proxer][g] + \
                                    self.phi[proxer][g] - phibar[g]

            # temporary value for x, overwritten by prox
            for a in proxer.agents:
                for g in self.xs[a].viewkeys():
                    self.xs[a][g] = self.xs[a][g] - xtild[g] - u[g]

            # temporary value for phi, overwritten by prox
            for g in self.phi[proxer].viewkeys():
                self.phi[proxer][g] = phibar[g] - self.w[proxer][g]

            # need to update private values
            xst, self.phi[proxer] = proxer.prox(self.xs, self.phi[proxer])
            self.xs.update(xst)

            phi_count.add_vals(self.phi[proxer])
            for x in xst.viewvalues():
                xs_count.add_vals(x)

        return xs_count, phi_count

    def displeasure(self, scaling, phi):
        """ Return the total and count of the displeasures of each agent, after
            scaling and taking the positive part of x
        """
        disp = AvgCounter()
        for p in self.proxers:
            for a in p.agents:
                x = dict(self.xs[a])
                for g in x:
                    x[g] = x[g] * scaling[g]

                disp.add_vals({'disp': a.displeasure(x, phi)})
        return disp


# todo: instead of dicts, we might store the variables internally with a
# more efficient structure with the same interface as a dict (numpy arrays
# inside)
# todo: slots this guy
class Proxer(object):
    """ Evaluates the prox operator related to one or more agents.
        Right now, only works for exchange markets.
    """

    def __init__(self, agents):
        self.agents = agents
        self._xs = defaultdict(lambda: defaultdict(cvx.Variable))
        self._phi = defaultdict(cvx.Variable)  # make sure these get touched
        # before the init is done!
        self._constr = []

        if isinstance(agents, Agent):
            agents = [agents]

        for a in agents:
            self._constr.extend(a.constr(self._xs[a], self._phi))

        # as soon as the constraints are created, the local variables are
        # touched in the defaultdict, so we know which variables this proxer
        # is interested in.

        # add positivity constraints
        for a, x in self._xs.iteritems():
            for g, v in x.iteritems():
                self._constr.append(v >= 0)

    def prox(self, x0, phi0):
        terms = []
        for a, x in self._xs.iteritems():
            for g, v in x.iteritems():
                terms.append(v - x0[a][g])

        for g, v in self._phi.iteritems():
            terms.append(v - phi0[g])

        prob = cvx.Problem(cvx.Minimize(cvx.norm2(cvx.vstack(*terms))),
                           self._constr)
        prob.solve(solver=cvx.SCS, verbose=False)
        assert prob.status == 'optimal'

        xs = {}
        for a, x in self._xs.iteritems():
            # take the positive part of the good allocations. (they should
            # be positive by the constraints anyway, but do this to polish
            # solution
            xs[a] = {g: max(v.value, 0) for g, v in x.iteritems()}
        phi = {g: v.value for g, v in self._phi.iteritems()}

        return xs, phi
