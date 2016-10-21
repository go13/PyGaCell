import random


class Operation:
    def __init__(self, hubs):
        self.hubs = hubs

    def calc(self):
        return None

    @classmethod
    def random_operation(cls, hubs):
        return {
            0: OpLink.random_operation,
            1: OpSum.random_operation,
        }[random.randint(0, 1)](hubs)


class OpLink(Operation):
    hub = None

    @classmethod
    def random_operation(cls, hubs):
        op_link = OpLink(hubs)

        hub_ind = random.randint(0, len(hubs))
        op_link.hub = hubs[hub_ind]

        return op_link

    def calc(self):
        return self.hub.calc()


class OpSum(Operation):
    @classmethod
    def random_operation(cls, hubs):
        op_sum = OpSum(hubs)
        return op_sum

    def calc(self):
        return sum([h.calc() for h in self.hubs])


class Hub:
    def __init__(self):
        self.outs = []
        self.val = None
        self.src = None

    def calc(self):
        return self.val if self.src is None else self.src.calc()


class Matcher:
    def match(self, l_tree, r_tree):
        pass


class Cell:
    def __init__(self, params):
        self.rating = None
        self.params = params
        self.inps = [Hub() for i in range(0, params.i_num)]
        self.outs = [Hub() for i in range(0, params.o_num)]

    @classmethod
    def create(cls, params):
        cell = Cell(params)

        for ot in cell.outs:
            ot.src = Operation.random_operation(cell.inps)

        return cell

    @classmethod
    def cross(cls, params, m, f):
        cell = Cell(params)

        # magic

        return cell

    def calc(self, inps):
        self.set_inputs(inps)

        results = [ot.calc() for ot in self.outs]

        self.rating = self.params.fn(results)

    def get_outputs(self):
        return [ot.val for ot in self.outs]

    def set_inputs(self, inps):
        for i in range(0, self.params.i_num):
            self.inps[i].val = inps[i]

    def mutate(self):
        pass
