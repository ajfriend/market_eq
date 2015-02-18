import collections
import random


def rand_tuple(population, k, required_inds=None):
    """
    Return a random k-tuple of unique elements selected from population.
    :param population: list or int. if n, then xrange(n)
    :param k: number of elements in tuple
    :param required_inds: list of elements which much be in the final tuple
    :return: tuple of k unique elements
    """
    if isinstance(population, int):
        population = xrange(population)

    if required_inds is None:
        required_inds = []
    if not isinstance(required_inds, collections.Iterable):
        required_inds = [required_inds]

    t = set(random.sample(population, k)) - set(required_inds)

    t = required_inds + list(t)
    return tuple(t[:k])
