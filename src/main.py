import random
from math import exp

from ga import GA, Params

print("PyGACell")


def fn(cell, inputs, outputs):
    x = inputs[0]
    y = - x * x + 4

    res = outputs[0]

    rating = exp(-(res - y) * (res - y))

    print "x = ", x, " y = ", y, " res = ", res, " rating = ", rating

    return rating

ga = GA(Params(2, 1, fn, 50, 10, 1))

for i in range(1000):
    print "step - ", i
    x = (random.random() - 0.5) * 4
    ga.step([x, x])
    print
