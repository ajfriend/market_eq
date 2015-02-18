# import sys
# import os
# sys.path.insert(0, os.path.abspath('.'))

from market_eq.market import gen_market, Market, gen_market2
from market_eq import utility as util
from market_eq.solvers import admm_solver, cvxpy_solver
from market_eq.agent import Agent


# def test4():
#     market = gen_market(10, 10, 4)
#
#     xs, phi = cvxpy_solver(market)
#     print market.check_sol(xs, phi)
#     xs, phi = market.polish_sol(xs, phi)
#     print market.check_sol(xs, phi)
#
#
#     xs, phi = admm_solver(market)


def test5():
    market = gen_market2(10, 10, 4)

    print market

    xs, phi = cvxpy_solver(market)
    print market.check_sol(xs, phi)
    market.polish_sol(xs, phi)
    print market.check_sol(xs, phi)

    xs, phi = admm_solver(market)

    return xs, phi



#
#
# def test3():
#     util1 = util.Linear({'apples': 2, 'oranges': 1})
#     endow1 = {'apples': 1, 'oranges': 2}
#     a1 = Agent(util1, endow1)
#
#     util2 = util.Linear({'apples': 1, 'oranges': 2})
#     endow2 = {'apples': 4}
#     a2 = Agent(util2, endow2)
#
#     market = Market([a1, a2])
#
#     #p = Proxer([a2])
#     #a = Accountant(p)
#     #a.step(defaultdict(float), defaultdict(float))
#
#     admm_solver(market)
#
#
# def test():
#     util1 = util.Linear({'apples': 2, 'oranges': 1})
#     endow1 = {'apples': 1, 'oranges': 2}
#     a1 = Agent(util1, endow1)
#
#     util2 = util.Linear({'apples': 1, 'oranges': 2})
#     endow2 = {'apples': 4}
#     a2 = Agent(util2, endow2)
#
#     market = Market([a1, a2])
#
#     print(market.goods())
#
#     print(market.desired())
#
#     print a2.demand({'apples': 1, 'oranges': 1})
#
#     print(market.sane())
#     print(market.really_sane())
#
#     xs, phi = cvxpy_solver(market)
#
#     print market.check_sol(xs, phi)
#     xs, phi = market.polish_sol(xs, phi)
#     print market.check_sol(xs, phi)
#
#     print market.relative_util(xs, phi)
#
#     # print('making the proxer')
#     # p = Proxer([a1, a2])
#     # x0 = {a1: {'apples': 0, 'oranges': 0}, a2: {'apples': 0, 'oranges': 0}}
#     # phi0 = {'apples': 0, 'oranges': 0}
#     # xs, phi = p.prox(x0, phi0)
#     #
#     # print market.check_sol(xs, phi)
#     # xs, phi = market.polish_sol(xs, phi)
#     # print market.check_sol(xs, phi)
#     #
#     # a = Accountant(p)
#     # x, phi = a.step(defaultdict(float), defaultdict(float))
#     # print x
#     # print phi
#
#
#     # market = gen_market(100, 100, 10)
#     # s = cvxpy_solver(market)
#     #
#     # print market.check_sol(s)
#     # s = market.polish_sol(s)
#     # print market.check_sol(s)
#     #
#     # print market.relative_util(s[0], s[1])
#
# def test2():
#     util1 = util.Linear({'apples': 2, 'oranges': 1})
#     endow1 = {'apples': 1, 'oranges': 2}
#     a1 = Agent(util1, endow1)
#
#     util2 = util.Linear({'apples': 1, 'oranges': 2})
#     endow2 = {'apples': 4}
#     a2 = Agent(util2, endow2)
#
#     market = Market([a1, a2])
#     xs, phi = cvxpy_solver(market)
#
#     print market.check_sol(xs, phi)
#     xs, phi = market.polish_sol(xs, phi)
#     print market.check_sol(xs, phi)
#
#
#     # p = Proxer([a1, a2])
#     #
#     # a = Accountant(p)
#     # a.step(defaultdict(float), defaultdict(float))
#
if __name__ == '__main__':
    xs, phi = test5()

