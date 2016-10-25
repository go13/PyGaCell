from cell import Cell
from random import random


class Params:
    def __init__(self, i_num, o_num, fn, population_size=50, untouchable_number=10, mutation_probability=0.1):
        self.mutation_probability = mutation_probability
        self.population_size = population_size
        self.untouchable_number = untouchable_number
        self.i_num = i_num
        self.o_num = o_num
        self.fn = fn


class GA:
    def __init__(self, params):
        self.params = params
        self.population = [Cell.create(params) for i in range(params.population_size)]

    def step(self):
        self.calc().crossover().mutate()

    def calc(self):
        for i in self.population:
            i.rate()

        self.population = sorted(self.population, key=lambda x: x.rating, reverse=True)

        return self

    def mutate(self):
        for i in self.population:
            i.mutate()

        return self

    def crossover(self):
        new_population = self.population[:self.params.untouchable_number]

        for i in range(self.params.population_size - self.params.untouchable_number):
            m = self.get_random_best()
            f = self.get_random_best()

            cell = Cell.cross(self.params, m, f)

            new_population += [cell]

        self.population = new_population

        return self

    def get_random_best(self):
        total_rating = sum([x.rating for x in self.population])

        p = total_rating * random()

        for x in self.population:
            r = x.rating
            if p < r:
                return x
            else:
                p = p - r

        return None

