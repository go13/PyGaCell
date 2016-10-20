from ga import GA, Params

print("PyGACell")


def fn(x):
    return 1

ga = GA(Params(10, 1, fn))

for i in range(1000):
    ga.step()
