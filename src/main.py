import random
from math import exp

from ga import GA, Params

print("PyGACell")


def fn(cell, experiment_number):
    x = (random.random() - 0.5) * 4
    cell.set_inputs([x, x])

    res = cell.calc()[0]

    y = - x * x + 4

    rating = exp(-(res - y) * (res - y))

    #if experiment_number == 1:
    #    print "x = ", x, " y = ", y, " res = ", res, " rating = ", rating

    return rating

ga = GA(Params(2, 1, fn, 20, 4, 1, 100))

for i in range(1000):
    print "step - ", i
    ga.calc()

    print ga.population[0].rating

    ga.grow()
    print
