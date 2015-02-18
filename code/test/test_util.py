from market_eq import utility as util
import numpy as np
from collections import defaultdict
import cvxpy as cvx

tol = 1e-8
tol_util = 1e-1

util_list = [util.Linear, util.CES, util.CobbDouglas, util.Logarithmic]


def gen_util(util_class):
    n = 10
    r = 5
    #util_fn = random.choice(util_list)
    util_fn = util_class.rand(r, n)

    phi = {str(k): np.random.rand() for k in xrange(n)}
    log_cash = np.random.rand()

    return util_fn, phi, log_cash


def util_suite(util_fn, phi, log_cash):
    inc = np.random.rand()
    phi2 = {k: v+inc for k, v in phi.iteritems()}

    util1, dem1 = util_fn.demand(phi, log_cash)
    util2, dem2 = util_fn.demand(phi2, log_cash+inc)

    # check that the demand is homogeneous of degree 0
    assert abs(util1-util2) <= tol

    # check that the keys are the same
    assert dem1.viewkeys() == dem2.viewkeys()
    # check that the demand values are the same
    for k in dem1:
        assert abs(dem1[k] - dem2[k]) <= tol

    # check that eval and demand give the same value
    assert abs(util1 - util_fn.eval(dem1)) <= tol

    # check that demand positive
    for k in dem1:
        assert dem1[k] >= 0

    # check that demand bounded by available cash
    cash = np.exp(log_cash)
    assert sum(np.exp(phi[g])*dem1[g] for g in dem1) <= cash + tol

    # check that all cash is used (walras' law)
    cash = np.exp(log_cash)
    assert abs(sum(np.exp(phi[g])*dem1[g] for g in dem1) - cash) <= tol

    # check that the constraint violations are small or negative
    for v in util_fn.constr(dem1, phi, log_cash):
        assert v <= tol

    # solve an opt problem and check that it is close
    x = defaultdict(cvx.Variable)
    constr = util_fn.constr(x, phi, log_cash)
    tot = 0
    for g in x:
        constr.append(x[g] >= 0)
        tot += x[g]*np.exp(phi[g])

    constr.append(tot <= np.exp(log_cash))
    cvx.Problem(cvx.Minimize(0), constr).solve(solver=cvx.SCS, verbose=False)
    for g in x:
        x[g] = x[g].value

    # check that two sols have relatively close utilities
    assert abs((util_fn.eval(x) - util_fn.eval(dem1))/util_fn.eval(dem1)) <=\
                tol_util


    # check that two sols have relatively close utilities
    x = get_cvx_demand(util_fn, phi, log_cash)
    assert abs((util_fn.eval(x) - util_fn.eval(dem1))/util_fn.eval(dem1)) <=\
                tol_util


def get_cvx_demand(util_fn, phi, log_cash):
    x = defaultdict(cvx.Variable)
    obj = cvx.Maximize(util_fn.cvx_eval(x))
    tot = 0
    constr = []
    for g in x:
        constr.append(x[g] >= 0)
        tot += x[g]*np.exp(phi[g])

    constr.append(tot <= np.exp(log_cash))
    cvx.Problem(obj, constr).solve(solver=cvx.SCS, verbose=False)
    for g in x:
        x[g] = x[g].value

    return x


def test_utils():
    for uc in util_list:
        for i in range(5):
            util_fn, phi, log_cash = gen_util(uc)
            yield util_suite, util_fn, phi, log_cash


# def test_utils2():
#     for uc in util_list:
#         for i in range(5):
#             util_fn, phi, log_cash = gen_util(uc)
#             util_suite(util_fn, phi, log_cash)
#
# if __name__ == '__main__':
#     test_utils2()
