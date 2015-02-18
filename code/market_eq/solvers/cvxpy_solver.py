from collections import defaultdict
import cvxpy as cvx


def cvxpy_solver(market):
    if not market.sane():
        raise Exception('The solver must be given a sane market.')

    xs = defaultdict(lambda: defaultdict(cvx.Variable))
    phi = defaultdict(cvx.Variable)

    constr = []
    good_constr = defaultdict(float)
    for a in market.agents:
        # utility function constraints
        constr.extend(a.constr(xs[a], phi))
        # now, all the local goods variables have been touched

        constr.extend(v >= 0 for v in xs[a].itervalues())

        # tally up global resources
        for g, v in xs[a].iteritems():
            good_constr[g] += xs[a][g]

    # global resource limit
    constr.extend(good_constr[g] <= b for g, b in market.goods.iteritems())

    prob = cvx.Problem(cvx.Minimize(0), constr)
    prob.solve(solver=cvx.SCS, verbose=True)

    xs = {a: {g: v.value for g, v in x.iteritems()} for a, x in xs.iteritems()}
    phi = {g: v.value for g, v in phi.iteritems()}

    return xs, phi
