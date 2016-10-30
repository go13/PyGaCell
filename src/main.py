import random
from math import exp

from ga import GA, Params

print("PyGACell")


def fn(cell, experiment_number):
    x = (random.random() - 0.5) * 10
    cell.set_inputs([x, x])

    res = cell.calc()[0]

    y = -x * x - 4

    rating = exp(-(res - y) * (res - y) / 2)

    #if experiment_number == 1:
    #    print "x = ", x, " y = ", y, " res = ", res, " rating = ", rating

    return rating

ga = GA(Params(2, 1, fn, 50, 20, 1, 10, 10, 100))

for i in range(1000):
    print "step - ", i
    ga.calc()

    cell = ga.population[0]
    print "rating = ", cell.pure_rating, " hub number = ", cell.get_hub_number()
    print cell
    ga.grow()
    print
