from ga import GA, Params

print("PyGACell")


def fn(x):
    print x
    return 1

ga = GA(Params(3, 2, fn, 5, 1))

for i in range(1000):
    ga.step([1, 2, 3])
