from market_eq.market import gen_market, Market, gen_market
from market_eq import utility as util
from market_eq.solvers import admm_solver, cvxpy_solver


def test():
    market = gen_market(4, 2)

    xs, phi = cvxpy_solver(market)

    print 'Before polishing'
    print 'tuple of residuals: ', market.check_sol(xs, phi)

    for a, x in xs.iteritems():
        print a, '\nx: ', x, '\ndispleasure: ', a.displeasure(x, phi)

    market.polish_sol(xs, phi)

    print 'after polishing'
    print 'tuple of residuals: ', market.check_sol(xs, phi)

    for a, x in xs.iteritems():
        print a, '\nx: ', x, '\ndispleasure: ', a.displeasure(x, phi)