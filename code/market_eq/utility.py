import numpy as np
import operator
import cvxpy as cvx
from abc import ABCMeta, abstractmethod
from itertools import izip

from market_eq import helper

"""
TODO: should the methods sanitize the input? for the eval method,
for example, should we remove negative entries?
todo: should the eval and other functions allow for zero entries in the dict to
just be left out? this would mess up the convenience of using the defaultdicts
of cvxpy variables
"""


class UtilityFunction(object):
    """ represents a utility function.
    """
    __metaclass__ = ABCMeta
    # for slots to work, every object in the inheritance
    # chain must have slots
    __slots__ = ()


    @abstractmethod
    def eval(self, x):
        """
        Evaluate the utility function at x. x should be a dictionary which
        contains keys for all the goods this utility function takes as input.
        If the dictionary values are numbers, return a number. If they are
        cvxpy variables, then return a cvxpy expression.
        """
        pass

    @abstractmethod
    def constr(self, x, phi, log_cash):
        """
        Return a list of the constraints corresponding to this utility
        function.
        :math:`\log(\nabla u(x)^T x) - \log( \nabla_j u(x) ) + \phi_j -
        \log{\sum_k b_{ik} e^{\phi_k} } \geq 0`

        If the input are constants, return the positive violation of the
        constraint, or 0 if the constraint is not violated.
        """
        pass

    @abstractmethod
    def demand(self, phi, log_cash):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def cvx_eval(self, x):
        """ return cvxpy expression for the (possibly transformed)
        utility function for computing the demand of this function
        in isolation
        """
        pass


class Linear(UtilityFunction):
    """
    u(x) = a^T x
    """
    __slots__ = 'goods', 'a'

    def __init__(self, goods, a):
        # todo validate a. each value should be positive
        # copy the data so the util owns it
        # numpy arrays will be more space efficient than tuples or dicts
        self.goods = np.array(goods)
        self.a = np.array(a)

    def __repr__(self):
        return self.__class__.__name__+"({},{})".format(self.goods, self.a)

    def eval(self, x):
        return sum(x[g]*a for g, a in izip(self.goods, self.a))

    def cvx_eval(self, x):
        return self.eval(x)

    def constr(self, x, phi, log_cash):
        #compute expr1 just once to save time. not sure if this is true, though
        expr1 = cvx.log(self.eval(x))

        def to_constant(x):
            """
            return violation if constant, constraint if variable"""
            return -x.value if x.is_constant() else x >= 0

        tmp = [to_constant(expr1 - np.log(a) + phi[g] - log_cash)
               for g, a in izip(self.goods, self.a)]

        return tmp

    #todo fix this demand function. do we need dictionaries?
    def demand(self, phi, log_cash):
        cash = np.exp(log_cash)

        bang_per_buck = {g: a/np.exp(phi[g])
                         for g, a in izip(self.goods, self.a)}

        g_max = max(bang_per_buck.iteritems(), key=operator.itemgetter(1))[0]
        util = bang_per_buck[g_max]*cash
        dem = {g: 0 for g in self.goods}
        dem[g_max] = cash/np.exp(phi[g_max])
        return util, dem

    @staticmethod
    def rand(population, k, required_inds=None):
        """ Generate a random utility function of this type.
        The utility is a function of n distinct goods chosen from 'pool'.
        If pool is an integer, 'good' keys are chosen from range(pool)
        """

        goods = helper.rand_tuple(population, k, required_inds)
        a = np.random.rand(k)

        return Linear(goods, a)


#todo update CES
class CES(UtilityFunction):
    """TODO: what about value of rho? for rho < -1, can we still do Fisher?
    """
    def __init__(self, a, rho=.5):
        if rho != .5:
            raise ValueError('For now, rho must be 1/2.')
        self.rho = rho
        self.a = dict(a)

    def __repr__(self):
        return self.__class__.__name__+"({},{})".format(self.rho, self.a)

    @property
    def goods(self):
        return self.a.viewkeys()

    def eval(self, x):
        """
        Evaluate the utility function at x. x should be a dictionary which
        contains keys for all the goods this utility function takes as input.
        If the dictionary values are numbers, return a number. If they are
        cvxpy variables, then return a cvxpy expression.
        """
        return sum(self.a[g]*(x[g]**self.rho)
                   for g in self.a)**(1/self.rho)

    def cvx_eval(self, x):
        if self.rho != .5:
            raise ValueError('need to implement general powers.')
        return sum(self.a[g]*cvx.sqrt(x[g])
                   for g in self.a)

    def constr(self, x, phi, log_cash):
        expr1 = cvx.log(sum(a*cvx.sqrt(x[g]) for g, a in self.a.iteritems()))

        def to_constant(x):
            """return violation if constant, constraint if variable"""
            return -x.value if x.is_constant() else x >= 0

        return [to_constant(expr1 - np.log(a) + (1-self.rho)*cvx.log(x[g]) +
                            phi[g] - log_cash)
                for g, a in self.a.iteritems()]

    def demand(self, phi, log_cash):
        cash = np.exp(log_cash)

        r = self.rho/(self.rho-1.0)
        dem = {g: (np.exp(phi[g])**r)*(a**(1-r))
               for g, a in self.a.iteritems()}
        tmp_sum = sum(dem.itervalues())
        dem = {g: cash*v/(tmp_sum*np.exp(phi[g])) for g, v in dem.iteritems()}

        util = self.eval(dem)
        return util, dem

    @staticmethod
    def rand(n, pool):
        """ Generate a random utility function of this type.
        The utility is a function of n distinct goods chosen from 'pool'.
        If pool is an integer, 'good' keys are chosen from
        [str(a) for a in range(pool)]
        """
        a = {str(k): np.random.rand()
             for k in np.random.choice(pool, n, replace=False)}
        return CES(a, rho=.5)


#todo update CobbDouglas
class CobbDouglas(UtilityFunction):
    def __init__(self, a):
        self.a = dict(a)
        # TODO: check that a is positive and sums to 1

    def __repr__(self):
        return self.__class__.__name__+"({})".format(self.a)

    @property
    def goods(self):
        return self.a.viewkeys()

    def eval(self, x):
        """
        Evaluate the utility function at x. x should be a dictionary which
        contains keys for all the goods this utility function takes as input.
        If the dictionary values are numbers, return a number. If they are
        cvxpy variables, then return a cvxpy expression.
        """
        return reduce(operator.mul,
                      (x[g]**a for g, a in self.a.iteritems()), 1)

    def cvx_eval(self, x):
        return sum(a*cvx.log(x[g]) for g, a in self.a.iteritems())

    def constr(self, x, phi, log_cash):
        def to_constant(x):
            """return violation if constant, constraint if variable"""
            return -x.value if x.is_constant() else x >= 0

        return [to_constant(cvx.log(x[g]) - np.log(a) + phi[g] - log_cash)
                for g, a in self.a.iteritems()]

    def demand(self, phi, log_cash):
        cash = np.exp(log_cash)
        tau = cash/sum(self.a.viewvalues())

        dem = {g: tau*a/np.exp(phi[g]) for g, a in self.a.iteritems()}
        util = self.eval(dem)

        return util, dem

    @staticmethod
    def rand(n, pool):
        """ Generate a random utility function of this type.
        The utility is a function of n distinct goods chosen from 'pool'.
        If pool is an integer, 'good' keys are chosen from
        [str(a) for a in range(pool)]
        """
        a = {str(k): np.random.rand()
             for k in np.random.choice(pool, n, replace=False)}
        total = sum(a.viewvalues())
        a = {g: v/total for g, v in a.iteritems()}
        return CobbDouglas(a)


# class Leontief(UtilityFunction):
#     """ how to add a descriptor that these don't work on Arrow-Debreu?
#     """
#     pass
#
#
# class FracPower(UtilityFunction):
#     pass
#
#

#todo update the rest of Logarithmic
class Logarithmic(UtilityFunction):
    __slots__ = 'goods', 'a', 'b'

    def __init__(self, goods, a, b):
        self.goods = np.array(goods)
        self.a = np.array(a)
        self.b = np.array(b)

    def eval(self, x):
        return sum(a*np.log(x[g] + b)
                   for g, a, b in izip(self.goods, self.a, self.b))

    def constr(self, x, phi, log_cash):
        def to_constant(x):
            """return violation if constant, constraint if variable"""
            return -x.value if x.is_constant() else x >= 0

        expr1 = cvx.log(sum(a - a*b*cvx.inv_pos(x[g] + b)
                            for g, a, b in izip(self.goods, self.a, self.b)))
        return [to_constant(expr1 - np.log(a) + cvx.log(x[g] + b) + phi[g] - log_cash)
                for g, a, b in izip(self.goods, self.a, self.b)]

    def demand(self, phi, log_cash):
        p = {g: np.exp(phi[g]) for g in self.goods}
        cash = np.exp(log_cash)

        goods_ord, taus_ord = zip(*sorted(((g, b*p[g]/a)
                                           for g, a, b in izip(self.goods, self.a, self.b)),
                                          key=lambda x: x[1]))

        # todo fix this
        a = dict(zip(self.g, self.a))
        b = dict(zip(self.g, self.b))

        fill = taus_ord*np.cumsum([a[g] for g in goods_ord]) - \
               np.cumsum([b[g]*p[g] for g in goods_ord])

        if fill[-1] < cash:
            i = len(self.goods)
        else:
            i = next(x[0] for x in enumerate(fill) if x[1] >= cash)
        tau = (cash + sum(b[g]*p[g] for g in goods_ord[:i]))/sum(a[g] for g in goods_ord[:i])
        dem = {g: max(0, tau*a[g]/p[g] - b[g]) for g in self.goods}
        util = self.eval(dem)

        return util, dem

    def __repr__(self):
        return self.__class__.__name__+"({},{},{})".format(self.goods, self.a,
                                                           self.b)

    def cvx_eval(self, x):
        return sum(a*cvx.log(x[g] + b)
                   for g, a, b in izip(self.goods, self.a, self.b))

    @staticmethod
    def rand(population, k, required_inds=None):
        """ Generate a random utility function of this type.
        The utility is a function of n distinct goods chosen from 'population'.
        If population is an integer, k keys are chosen from range(population)
        """

        goods = helper.rand_tuple(population, k, required_inds)
        a = (np.random.rand() for _ in xrange(k))
        b = (np.random.rand() for _ in xrange(k))

        return Logarithmic(goods, a, b)